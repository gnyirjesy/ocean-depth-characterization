from flask import Flask, request, Response
from io import StringIO
import mysql.connector
from  model_inference.nn_inference import run_inf_model
import datetime
# from werkzeug.wrappers import Response
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/getPlotCSV')
def download_log():
    model_output = request.headers.get('model_data')
    csv_string = f"depth,chla_pred,{model_output}"
    split = csv_string.split(',')
    final_csv = "\n".join([",".join(split[i:i+2]) for i in range(0,len(split),2)])
    return Response(
        final_csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})

@app.route('/run_model/<date>/<lat>/<lon>/<chlor>/<sst>/<pic>/<aph>/<par>', methods=['GET'])
def run_model(date, lat, lon, chlor, sst, pic, aph, par):
    print(date)
    date_obj = datetime.datetime.strptime(date, '%Y%m%d')
    print(date_obj)
    # COVNERT DATE TO RADIANS!!!
    j_days = date_obj.timetuple().tm_yday
    date_rad = (j_days/365)*(2*math.pi)
    print("DATE CONVERTED", date_rad)


    model_output = run_inf_model(
        lat=float(lat),
        lon=float(lon),
        date=float(date_rad),
        chlor=float(chlor),
        sst=float(sst),
        pic=float(pic),
        aph=float(aph),
        par=float(par)
    )

    
    list_of_depth_dicts = []
    cleaned_model_output = model_output.tolist()
    # todo: convert x axis to normalized depth
    for i, pred in enumerate(cleaned_model_output):
        depth_dict = {}
        depth_dict['x'] = float(i/25)
        depth_dict['y'] = pred
        list_of_depth_dicts.append(depth_dict)

    return {
        'model_data': list_of_depth_dicts
    }

@app.route('/sat_pull/<date>/<lat>/<lon>', methods=['GET'])
def get_sat_data(date=None,lat=None, lon=None):

    month = date[4]
    if month == '3':
        month_suff = 'march'
    elif month == '9':
        month_suff = 'sept'
    else:
        print(f"Unkown month: {month}")

    cleaned_data = []
    mydb = mysql.connector.connect(
    host="34.134.186.213",
    user="root",
    password="Student2011",
    database='sat_test_data_1'
    )

    mycursor = mydb.cursor(dictionary=True)

    sat_data = []
    query = f"""
    SELECT lat, lon, 
        POW(69.1 * (lat - {lat}), 2) +
        POW(69.1 * ({lon} - lon) * COS(lat / 57.3), 2) AS distance,
        sat_data_{month_suff}.*
    FROM 
        sat_data_{month_suff}
    WHERE date = '{date}' 
    ORDER BY 
        distance LIMIT 1
    """
    print(query)

    mycursor.execute(query)
    sat_data = mycursor.fetchall()

    for key, value in sat_data[0].items():
        if key == 'distance':
            continue
        cleaned_data.append(
            {
                'var': key,
                'value': value
            
            }
        )

    print(cleaned_data)
    return {
        'sat_data': cleaned_data
    }
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)