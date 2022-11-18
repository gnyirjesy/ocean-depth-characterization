# perform inference using the specified model path on 25 normalized points from zero to one
import numpy as np
import pandas as pd
import pickle
import keras
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.interpolate import interp1d
import warnings



# set model path
MODEL_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/model_files/nn_multireg_108283'
SCALER_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/model_files/standardscaler_108283.pkl'


class ChlaPredictor():

    def __init__(self, model_path , scaler_path):
        
        warnings.filterwarnings('ignore')
        # import necessary files
        print('Loading model...')
        self.model = load_model(model_path)
        self.scaler = pickle.load(open(scaler_path, 'rb'))
        print('Model loaded successfully')

        # set up kmeans for later
        self.centers = np.array([[0.41317453, 0.46748513, 0.5188263 , 0.55383564, 0.58045696,
                                    0.58820526, 0.57298827, 0.53097843, 0.47768674, 0.41734389,
                                    0.35210721, 0.28540239, 0.23338234, 0.18364529, 0.14661946,
                                    0.11272519, 0.08926945, 0.070071  , 0.0576842 , 0.04639839,
                                    0.03605629, 0.03086947, 0.02797389, 0.02666722, 0.02564945],
                                [0.10747704, 0.11232824, 0.12416936, 0.14590532, 0.19098353,
                                    0.25143391, 0.31557576, 0.3778138 , 0.39809846, 0.39030771,
                                    0.35749554, 0.30671173, 0.25797338, 0.21325299, 0.17613028,
                                    0.14640923, 0.12038377, 0.09768159, 0.07939508, 0.0641688 ,
                                    0.05165149, 0.04251336, 0.03589103, 0.03072038, 0.02685341],
                                [0.94819012, 0.99308904, 1.02731265, 0.95491256, 0.78776714,
                                    0.60738444, 0.46215405, 0.35638285, 0.2792321 , 0.22171482,
                                    0.17823882, 0.14628394, 0.12463334, 0.10744187, 0.09367764,
                                    0.08226775, 0.07302317, 0.06549189, 0.05947828, 0.05468831,
                                    0.05050702, 0.0468269 , 0.04413142, 0.04092826, 0.03857374],
                                [0.58818818, 0.58583076, 0.59669966, 0.60978989, 0.61007765,
                                    0.59415282, 0.56115817, 0.5115877 , 0.45002541, 0.38337771,
                                    0.31698094, 0.25713183, 0.20664978, 0.16475079, 0.13189105,
                                    0.10709871, 0.08817151, 0.07348845, 0.06169837, 0.05202374,
                                    0.04407668, 0.03737277, 0.03151687, 0.02664956, 0.02245804],
                                [0.02434728, 0.02460363, 0.02581248, 0.02812329, 0.03187796,
                                    0.03727261, 0.04495509, 0.05575595, 0.07037495, 0.08910255,
                                    0.11114404, 0.13437359, 0.15886012, 0.17547859, 0.17721822,
                                    0.16539735, 0.14497307, 0.12034047, 0.09528552, 0.07258161,
                                    0.05346715, 0.03802479, 0.02601964, 0.01678069, 0.00998742],
                                [0.14894491, 0.15727387, 0.16281632, 0.17001331, 0.18123477,
                                    0.19650756, 0.21308114, 0.22705645, 0.23570769, 0.23681044,
                                    0.22765918, 0.2095035 , 0.18564293, 0.16008297, 0.13634142,
                                    0.11333204, 0.09254978, 0.07431426, 0.05888546, 0.04637136,
                                    0.03724998, 0.02995289, 0.02402373, 0.0192311 , 0.01539957]])
        self.kmeans = KMeans(n_clusters=6)
        self.kmeans.fit(self.centers)

    def make_inference(self, input_features):
        '''
        model prediction

        interpolation of results

        kmeans prediction and mixing
        '''
        # make input have dimensions for model
        try:
            in_dim = input_features.shape[1]
        except IndexError:
            input_features = np.array([input_features])
        scaled_features = self.scaler.transform(input_features)
        # make raw predictions
        preds = self.model.predict(scaled_features, verbose=0)
        int_preds = self.interpolate(preds)
        final_predictions = self.create_mixture(int_preds)
        return final_predictions
    
    def interpolate(self, predictions):
        
        n_points = 25
        # interpolate results
        xold = np.linspace(0, 1, 4)
        xnew = np.linspace(0, 1, n_points)
        int_predictions = list()
        for prediction in predictions:
            fp = interp1d(xold, prediction, kind='quadratic')
            int_predictions.append(fp(xnew))
        int_preds_df = pd.DataFrame(np.array(int_predictions), columns=['intpred_' + str(i) for i in range(n_points)])
        return int_preds_df
    
    def create_mixture(self, int_preds, mixture=0.2):
        n_points = 25

        kmeans_preds = self.kmeans.predict(int_preds.to_numpy())
        centers = self.kmeans.cluster_centers_
        final_predictions = list()
        for i, int_p in int_preds.iterrows():
            closest_center = centers[kmeans_preds[i], :]
            prediction = self.mix_vals(closest_center, int_p, perc_x1=mixture)
            final_predictions.append(prediction)
        fin_preds = np.array(final_predictions)
        return fin_preds
    
    def mix_vals(self, x1, x2, perc_x1=0.5):
        perc_x2 = 1-perc_x1
        return (x1*perc_x1) + (x2*perc_x2)