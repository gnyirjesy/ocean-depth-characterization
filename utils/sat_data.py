# Functions to assist with satellite data query and processing
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import xarray as xr
import os
from os.path import exists
import bisect
import calendar
import argparse


def get_filename(lookup_date, date_values, var_oceandata, period):
    """
    Description: Determine filename on oceandata based on the lookup date, variable, and period

    Inputs:
        date_values: list, list with all 8 day options
        lookup_date: datetime.date object, date of interest to pull in data for all locations
        var_oceandata: str, name of variable on oceandata
        period: str, period of interest {'day','8d','month'}

    Outputs:
        filename, str
    """
    if period == 'day':
        #Specify filename for daily data:
        # var_oceandata = 'CHL.chl_a'
        filename = "AQUA_MODIS."+str(lookup_date.year) + '{0:02d}'.format(lookup_date.month) + '{0:02d}'.format(lookup_date.day) \
            + ".L3m.DAY." + var_oceandata + ".4km.nc"
    elif period == '8d':
        #date list must be sorted to perform the bisection***
        #find day with the 8 day value file
        date_loc = bisect.bisect_right(date_values, pd.Timestamp(lookup_date))
        date_8d_start = date_values[date_loc-1]
        date_8d_end = date_values[date_loc] - timedelta(1)

        #Determine which file to open:
        filename = "AQUA_MODIS."+str(date_8d_start.year) + '{0:02d}'.format(date_8d_start.month) + '{0:02d}'.format(date_8d_start.day) \
            + "_" + str(date_8d_end.year) + '{0:02d}'.format(date_8d_end.month) + '{0:02d}'.format(date_8d_end.day)+".L3m.8D." + var_oceandata +".4km.nc"
    elif period == 'month':
        #monthly example:
        # AQUA_MODIS.20220101_20220131.L3m.MO.CHL.chlor_a.4km.nc 
        #Determine which file to open:
        filename = "AQUA_MODIS."+str(lookup_date.year) + '{0:02d}'.format(lookup_date.month) + '{0:02d}'.format(1) \
            + "_" + str(lookup_date.year) + '{0:02d}'.format(lookup_date.month) \
                + '{0:02d}'.format(calendar.monthrange(lookup_date.year, lookup_date.month)[1])+".L3m.MO."+var_oceandata+".4km.nc"
    return(filename)

def lookup_sat_value(latitude, longitude, filename, var_oceandata):
    """
    Description; Pull specific values of variable at given latitude and longitude

    Input:
        latitude: float, latitude of interest
        longitude: float, longitude of interest
        filename: str, path to file with satellite data
        var_name: str, name of the variable of interest
        var_oceandata: str, name of variable on oceandata

    Output:
        float, value of variable from satellite data
    """
    if exists(filename):
        ds = xr.open_dataset(filename)
        var_value_name = var_oceandata.split('.')[1]
        sat_val = ds.sel(lon=longitude, lat=latitude, method='nearest')
        if np.isnan(sat_val[var_value_name].values.item()):
            return_val = np.nan
        else:
            return_val = sat_val[var_value_name].values.item()
    else:
        return_val = np.nan
    return(return_val)

def query_data(filename, appkey_val, output_dir):
    """
    Description: Code to call the oceandata query

    Inputs: 
        filename: str, name of the file to pull from oceandata
        appkey_val: str, appkey from oceandata
        output_dir: str, location to store queried data
    
    Output:
        None (data stored in output directory)
    """

    current_folder = os.getcwd()
    command = "python oceandata_query.py " + filename +" --appkey "+appkey_val + " --odir " + current_folder + output_dir
    # print(command)
    os.system(command)

def get_sat_val(latitude, longitude, lookup_date, var_oceandata, period, date_values, appkey_val):
    """
    Description: Get the value of the variable from the satellite data

    Inputs:
        latitude: float, latitude of interest
        longitude: float, longitude of interest
        lookup_date: datetime.date object, date of interest to pull in data for all locations
        var_oceandata: str, name of variable on oceandata
        period: str, period of interest {'day','8d','month'}
        date_values: list, list with all 8 day options
        appkey_val: str, appkey from oceandata

    Outputs:
        float, satelitte value
    """
    
    #First try to query the daily data
    fname = get_filename(lookup_date, date_values, var_oceandata,period)
    query_data(fname, appkey_val, output_dir = '/temp/')
    sat_val = lookup_sat_value(latitude, longitude, './temp/'+fname, var_oceandata)
    #delete file to save space
    if exists('./temp/'+fname):
        os.system("rm ./temp/" + fname)
    return(sat_val)

def day_8d_month_impute(latitude, longitude, lookup_date, var_oceandata, date_values, appkey_val):
    """
     Description: Query and impute the satelitte data for a specific variable (first fill with
     daily value, then 8-day, then monthly average)

    Inputs:
        latitude: float, latitude of interest
        longitude: float, longitude of interest
        lookup_date: datetime.date object, date of interest to pull in data for all locations
        var_oceandata: str, name of variable on oceandata
        date_values: list, list with all 8 day options
        appkey_val: str, appkey from oceandata

    Outputs:
        float, satelitte value
    """

    sat_val = get_sat_val(latitude, longitude, lookup_date, var_oceandata, 'day', date_values, appkey_val)
    if np.isnan(sat_val):
        sat_val = get_sat_val(latitude, longitude, lookup_date, var_oceandata, '8d', date_values, appkey_val)
        if np.isnan(sat_val):
            sat_val = get_sat_val(latitude, longitude, lookup_date, var_oceandata, 'month', date_values, appkey_val)
    return(sat_val)

if __name__ == '__main__':
    print('this is working')
    parser = argparse.ArgumentParser(description='Pull satellite date for given latitude, longitude, date')
    parser.add_argument('latitude',type=float, help='latitude of interest')
    parser.add_argument('longitude',type=float, help='longitude of interest')
    parser.add_argument('year', type=int, help='year of interest')
    parser.add_argument('month', type=int, help='month of interest')
    parser.add_argument('day', type=int, help='day of interest')
    parser.add_argument('OceanDataVariable', type=str, help='variable of interest, options include CHL.chlor_a, FLH.ipar, etc.')
    parser.add_argument('appkey_val',type = str, help='NASA EarthData appkey')
    args = parser.parse_args()
    latitude = args.latitude
    longitude = args.longitude
    year = args.year
    month = args.month
    day = args.day
    lookup_date = datetime(year, month, day)
    oceandata_var = args.OceanDataVariable
    appkey_val = args.appkey_val
    date_values = []
    for i in range(2010,2023):
        # if i == 2010:  
        #     date_values_new = pd.date_range(start = datetime(i,1,2), end = datetime(i,12,31), freq='8D')
        # else:
        date_values_new = pd.date_range(start = datetime(i,1,1), end = datetime(i,12,31), freq='8D')
        date_values.extend(date_values_new)
    #Sort so the bisect works when used later
    date_values.sort()
    # print(get_filename(lookup_date, date_values, oceandata_var, 'day'))
    results = day_8d_month_impute(latitude, longitude, lookup_date, oceandata_var, date_values, appkey_val)
    print(results)
    # results.to_csv('./results.csv')
