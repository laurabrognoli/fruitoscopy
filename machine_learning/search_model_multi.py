from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn import cross_validation as cv
from sklearn import svm
import json

#MODULO 1
#LABELS SEPARATED FROM THE MATRIX


#loading data

tmpdata = np.genfromtxt('exit.csv', delimiter=' ')
X = np.nan_to_num(tmpdata)

# Creation of labels
tmpdata = np.genfromtxt('labels.csv', delimiter=',')
y = np.nan_to_num(tmpdata)


# Global variables to store parameters for BEST model
num_bin=0
max_mcc=0
model=' '
parameter=0
acc=0

def multimcc(t,p, classes=None):
    """ Matthews Correlation Coefficient for multiclass
    :Parameters:
        t : 1d array_like object integer 
          target values
        p : 1d array_like object integer 
          predicted values
        classes: 1d array_like object integer containing 
          all possible classes
    
    :Returns:
        MCC : float, in range [-1.0, 1.0]
    """

    # Cast to integer
    tarr = np.asarray(t, dtype=np.int)
    parr = np.asarray(p, dtype=np.int)
    
    
    # Get the classes
    if classes is None:
        classes = np.unique(tarr)
    
    nt = tarr.shape[0]
    nc = classes.shape[0]
    
    # Check dimension of the two array
    if tarr.shape[0] != parr.shape[0]:
        raise ValueError("t, p: shape mismatch")

    # Initialize X and Y matrices
    X = np.zeros((nt, nc))
    Y = np.zeros((nt, nc))

    # Fill the matrices 
    for i,c in enumerate(classes):
        yidx = np.where(tarr==c)
        xidx = np.where(parr==c)

        X[xidx,i] = 1
        Y[yidx,i] = 1

    # Compute the denominator
    denom = cov(X,X) * cov(Y,Y)
    denom = np.sqrt(denom)
    
    if denom == 0:
        # If all samples assigned to one class return 0
        return 0
    else:
        num = cov(X,Y)
        return num / denom


def confusion_matrix(t, p):
    """ Compute the multiclass confusion matrix
    :Parameters:
        t : 1d array_like object integer (-1/+1)
          target values
        p : 1d array_like object integer (-1/+1)
          predicted values
    
    :Returns:
        MCC : float, in range [-1.0, 1.0]
    """

    # Read true and predicted classes
    tarr = np.asarray(t, dtype=np.int)
    parr = np.asarray(p, dtype=np.int)
    
    # Get the classes
    classes = np.unique(tarr)

    # Get dimension of the arrays
    nt = tarr.shape[0]
    nc = classes.shape[0]
    # Check dimensions should match between true and predicted
    if tarr.shape[0] != parr.shape[0]:
        raise ValueError("t, p: shape mismatch")
    # Initialize Confusion Matrix C
    C = np.zeros((nc, nc))
    # Fill the confusion matrix
    for i in xrange(nt):
        ct = np.where(classes == tarr[i])[0]
        cp = np.where(classes == parr[i])[0]
        C[ct, cp] += 1
    # return the Confusion matrix and the classes
    return C, classes

def cov(x,y):
    nt = x.shape[0]
    xm, ym = x.mean(axis=0), y.mean(axis=0)
    xxm = x - xm
    yym = y - ym
    tmp = np.sum(xxm * yym, axis=1)
    ss = tmp.sum()
    return ss/nt
 
# function to test model & store values if BEST model
def model_run(predictions,y,model_name,val_num,bin_num,nb,maxm,model):
    mcc=multimcc(y, predictions)
    med=np.mean(mcc)
    if med>maxm:
        maxm=med
        parameter=val_num
        model=model_name
        nb=bin_number
    print(model_name,val_num, med)
    return nb, maxm, model,i    

# main loop to iterate models through all desired bins        
for bin_number in range(100,200,5):
    print(bin_number)
    #result of the binning, stat 
    stat, bin_edges, binnum = stats.binned_statistic(range(X.shape[1]), X, 'median', bins=bin_number) 

    ml_models = {'Rand_f': [100,500,1000],'Linear_d': [0],'Support_v':[10**-3,10**-2,10**-1,1,10,100,1000]}

    # loop to iterate through all model types for current bin number
    for key, value in ml_models.items():
        if key == 'Rand_f':
            for i in value:
                predictions= cv.cross_val_predict(RandomForestClassifier(n_estimators=i,n_jobs=-1), stat, y, cv=5)            
                num_bin, max_mcc, model, parameter= model_run(predictions,y,'RandomForest()',i,bin_number,num_bin,max_mcc,model)
        '''if key == 'Linear_d':
            for i in value:
                predictions= cv.cross_val_predict(LinearDiscriminantAnalysis(n_components=i), stat, y, cv=5)            
                num_bin, max_mcc, model, parameter= model_run(predictions,y,'LinearDiscriminantAnalysis()',i,bin_number,num_bin,max_mcc,model)'''
        if key == 'Support_v':
            for i in value:
                predictions= cv.cross_val_predict(svm.LinearSVC(C=i), stat, y, cv=5)            
                num_bin, max_mcc, model, parameter= model_run(predictions,y,'svm.LinearSVC()',i,bin_number,num_bin,max_mcc,model)     
              
print(max_mcc,model,num_bin,parameter,acc)

# make dictionary of BEST model
output = {'model': model, 'parameter': parameter, 'num_bins': num_bin, 'mcc': max_mcc}

# store dictionary in json file
with open('parameters.json', 'w') as f:
     json.dump(output, f)
             
