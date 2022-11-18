# training multiregression neural net model on entire final_norm_set.csv set
# author: Blake Hartung

# import libraries
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler

FINAL_NORM_SET_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/data/final_norm_set.csv'
OUTPUT_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/model_files/'

def main():

    # load data
    df = pd.read_csv(FINAL_NORM_SET_PATH)
    
    # gather features and labels
    feature_cols = ['latitude', 'longitude', 'date_doy_rad', 'sat_chl_month', 'sat_sst_month', 'sat_pic_month', 'sat_aph_443_month']
    label_bins = [1, 2, 3, 4]
    label_cols = ['norm_' + str(i) for i in label_bins]
    X_train = df[feature_cols]
    Y_train = df[label_cols]

    # declare model dimensions
    input_dim = X_train.shape[1]
    output_dim = Y_train.shape[1]

    # scale the features
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)

    # create and compile model
    nn_model = Sequential()

    nn_model.add(Dense(108, input_dim=input_dim, activation='relu'))
    nn_model.add(Dropout(0.3))
    nn_model.add(Dense(28, activation='relu'))
    nn_model.add(Dropout(0.3))
    nn_model.add(Dense(output_dim))

    nn_model.compile(loss='mse', optimizer='adam')

    #fit the model
    nn_model.fit(X_train, Y_train, epochs=15, batch_size=32, verbose=1)

    nn_model.save(OUTPUT_PATH + 'nn_multireg_108283')

    print()
    print(f'Model saved at: {OUTPUT_PATH}nn_multireg_108283')
    
    # save standard scaler
    pickle.dump(scaler, open(OUTPUT_PATH + 'standardscaler_108283.pkl', 'wb'))
    print('Scaler saved.')


if __name__ == '__main__':
    main()


