# training multiregression neural net model on entire final_norm_set.csv set
# author: Blake Hartung

# import libraries
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler

FINAL_NORM_SET_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/data/final_norm_set_10.csv'
OUTPUT_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/model_files/'

def main():

    # load data
    df = pd.read_csv(FINAL_NORM_SET_PATH)
    
    # gather features and labels
    feature_cols = ['latitude', 'longitude', 'date_doy_rad', 'sat_chl_month', 'sat_sst_month', 'sat_pic_month', 'sat_aph_443_month']
    label_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    label_cols = ['norm_' + str(i) for i in label_bins]
    X_train = df[feature_cols]
    Y_train = df[label_cols]

    # scale the features
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)

    # create and compile model
    models = {}
    for i in label_bins:
        models['xgb_depth_' + str(i)] = XGBRegressor()
        models['xgb_depth' + str(i)].fit(X_train, Y_train)

    print()
    print(f'Model saved at: {OUTPUT_PATH}xgb_multimodel_10')
    
    # save standard scaler
    pickle.dump(scaler, open(OUTPUT_PATH + 'standardscaler_xgb_10.pkl', 'wb'))
    print('Scaler saved.')


if __name__ == '__main__':
    main()