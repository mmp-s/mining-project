#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 18:29:39 2019

@author: note
"""

import pandas
import numpy as np
from sklearn import model_selection
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import matthews_corrcoef
from matplotlib.legend_handler import HandlerLine2D
from sklearn.metrics import make_scorer

import matplotlib.pyplot as plt

seed = 10

datasetTrain = pandas.read_csv("Dataset_processado/dataset_treino_processado.csv")
kfold = model_selection.StratifiedKFold(n_splits=10, random_state=seed)

X_train = datasetTrain.values[:, 0:8]
Y_train = datasetTrain.values[:, 8]

max_d = np.arange(5, 22)
rfc_mcc_train = []
rfc_mcc_val = []

for i, k in enumerate(max_d):
    print(" ----------> max_depth =", k)
    rfc = RandomForestClassifier(criterion='entropy', max_depth=k, n_estimators=21, random_state=seed)
    rfc = rfc.fit(X_train, Y_train)
    
    Y_pred_train = rfc.predict(X_train)
    
    mcc_train = matthews_corrcoef(Y_train, Y_pred_train)
    rfc_mcc_train.append(mcc_train)
    print("MCC train: %0.3f" %  rfc_mcc_train[i])
    
    resultsRFC = model_selection.cross_val_score(rfc, X_train, Y_train, cv=kfold, scoring=make_scorer(matthews_corrcoef))

    print('MCC k-fold mean:', resultsRFC.mean())
    
    rfc_mcc_val.append(resultsRFC.mean())
    
    Y_prediction = rfc.predict(X_train)
#    print("Clasification report:\n", classification_report(Y_train, Y_prediction))
#    print("Confussion matrix:\n", confusion_matrix(Y_train, Y_prediction))

line1, = plt.plot(max_d, rfc_mcc_train, 'b', label='Train score')
line2, = plt.plot(max_d, rfc_mcc_val, 'r', label='Validation score')

plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('MCC score')
plt.xlabel('max_depth')
plt.show()
