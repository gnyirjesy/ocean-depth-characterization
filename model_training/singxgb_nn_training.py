# training xgboost with multiregression neural net model on entire final_norm_set_11.csv set
# author: Blake Hartung, Josie Donnelly

# import libraries
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from xgboost import XGBRegressor
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler

FINAL_NORM_SET_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/data/final_norm_set_11.csv'
OUTPUT_PATH = 'C:/Users/johnc/Documents/Python Scripts/ocean-depth-characterization/model_files/'

def main():
    dim = 11
    # load data
    df = pd.read_csv(FINAL_NORM_SET_PATH)
    shape = df.shape
    
    # gather features and labels
    feature_cols = ['latitude', 'longitude', 'date_doy_rad', 'sat_chl_month', 'sat_sst_month', 'sat_pic_month', 'sat_par_month', 'sat_aph_443_month', 'norm_depth']
    label_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # create long dataframe
    dfl = df[['float', 'cycleNumber', 'latitude', 'longitude', 'date_doy_rad', 'sat_chl_month', 'sat_sst_month', 'sat_pic_month', 'sat_par_month', 'sat_aph_443_month'] + [f'norm_{i}' for i in range(dim)]]
    dfl = dfl.append([dfl] * 10).sort_values(by=['float', 'cycleNumber'], axis=0, ascending=True, ignore_index=True)
    dfl['norm_depth'] = [i / 10 for i in range(11)] * shape[0]
    dfl['chla'] = df[['norm_' + str(i) for i in label_bins]].to_numpy().reshape(-1)

    # separate variables
    X_train = dfl[feature_cols].to_numpy()
    y_train = dfl['chla'].to_numpy()
    # scale the features
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)

    # create and compile xgb model
    print('Fitting XGBoost Model...')
    xgbr = XGBRegressor(n_estimators=20, max_depth=12, colsample_bytree=0.7)
    xgbr.fit(X_train, y_train)
    tr_score = xgbr.score(X_train, y_train)
    print()
    print(f'XGB Model Fit: Train R2: {tr_score:.2f}')
    pickle.dump(xgbr, open(OUTPUT_PATH + 'xgb_11.model', 'wb'))
    print(f'XGB Model saved at: {OUTPUT_PATH}xgb_11.model')

    # create predictions for nn
    preds = xgbr.predict(X_train)
    X_train_nn = preds.reshape(shape[0], 11)
    Y_train_nn = df[['norm_' + str(i) for i in label_bins]].to_numpy()

    # compile nn
    print('Training nn...')
    nn = Sequential()
    nn.add(Dense(128, input_dim=X_train_nn.shape[1], activation='relu'))
    nn.add(Dropout(0.3))
    nn.add(Dense(128, activation='relu'))
    nn.add(Dropout(0.3))
    nn.add(Dense(Y_train_nn.shape[1]))
    nn.compile(loss='mse', optimizer='adam')

    nn_history = nn.fit(X_train_nn, Y_train_nn, epochs=8, batch_size=24, verbose=1)

    nn.save(OUTPUT_PATH + 'nn_1281283')
    print()
    print(f'Neural Net Model saved at: {OUTPUT_PATH}nn_1281283')
    
    # save standard scaler
    pickle.dump(scaler, open(OUTPUT_PATH + 'ss_11.pkl', 'wb'))
    print('Scaler saved.')


if __name__ == '__main__':
    main()