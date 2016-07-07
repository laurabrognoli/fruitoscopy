from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
from scipy import stats
from sklearn import svm
from sklearn.externals import joblib
import pickle
import json


with open('parameters.json') as data_file:
    dic = json.load(data_file)
bin_num = dic['num_bins']

tmpdata = np.genfromtxt('grapes_white_transpose.csv', delimiter=',')
X = np.nan_to_num(tmpdata)
test=X.transpose()

#MODULO 1
#LABELS SEPARATED FROM MATRIX THE

#MODULO2
#PROCESS THE DATA(BINNING)

#binning test spectrum,binned spectrum==test
test_data,bin_edges_ts,binnum_ts=stats.binned_statistic(range(test.shape[1]), test, 'median', bins=int(bin_num))

#MODULO3
#APPLY THE MODEL AND PRINT THE RESULT

a_result=joblib.load("model.pkl")

for i in test_data:
    print(a_result.predict(i.reshape(1,-1)))

