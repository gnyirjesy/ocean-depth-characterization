# train K Nearest Neighbors model for biome prediction
# Inputs:
# train_set: train dataframe with columns float_cycle, 'cluster', day_of_year_rad, latitude, longitude
# test_set: train dataframe with columns float_cycle, 'cluster', day_of_year_rad, latitude, longitude
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix, ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

ABS_PATH = os.path.dirname(os.getcwd())
TRAIN_CLUSTER_PATH = ABS_PATH + '/normalization_and_clustering/knn_data/knn_train.csv'
TEST_CLUSTER_PATH = ABS_PATH + '/normalization_and_clustering/knn_data/knn_test.csv'
CLUSTER_PICKLE_PATH = ABS_PATH + '/model_files/knearestneighbors_cluster_classification_simple'

def main():
    #read in data
    print('Reading in cluster data...')
    train_set = pd.read_csv(TRAIN_CLUSTER_PATH)
    test_set = pd.read_csv(TEST_CLUSTER_PATH)
    index_col = 'float_cycle'
    train_set = train_set.set_index([index_col])
    test_set = test_set.set_index([index_col])
    y_train, y_test = train_set['cluster'], test_set['cluster']
    x_train, x_test = train_set.drop('cluster', axis=1), test_set.drop('cluster', axis=1)
    #Model without season
    print('Training Model...')
    knn_simple = KNeighborsClassifier(n_neighbors = 6, weights='distance').fit(x_train[['day_of_year_rad', 'latitude', 'longitude']], y_train)
    print('Results:')
    # accuracy on X_test
    accuracy = knn_simple.score(x_test[['day_of_year_rad', 'latitude', 'longitude']], y_test)
    print(round(accuracy,5))
    #make predictions and view results
    #Move forward with model without season
    knn_predictions = knn_simple.predict(x_test[['day_of_year_rad', 'latitude', 'longitude']])
    cluster_names = train_set['cluster'].unique()
    cm = confusion_matrix(y_test, knn_predictions, labels=sorted(cluster_names))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(cluster_names))
    # plt.subplot(1,2,1)
    disp.plot()
    _ = plt.title('Confusion Matrix: KNN Biome Classifier')
    plt.show()
    #Save model
    pickle.dump(knn_simple, open(CLUSTER_PICKLE_PATH,'wb'))

if __name__ == '__main__':
    main()