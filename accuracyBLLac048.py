#!/usr/bin/env python
# coding: utf-8

## %matplotlib inline
import os
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from sklearn import metrics, model_selection
import xgboost as xgb
from xgboost.sklearn import XGBClassifier

data = pd.read_csv('input/BLLac-048-mjd.csv', names=['mjd','date','S','sigS'])
data.head()
data.info()

data['mjd'],class_names = pd.factorize(data['mjd'])
print(class_names)
print(data['mjd'].unique())

data['date'],_ = pd.factorize(data['date'])
data['S'],_ = pd.factorize(data['S'])
data['sigS'],_ = pd.factorize(data['sigS'])

X = data.iloc[:,:-1]
y = data.iloc[:,-1]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, random_state=123)

params = {
    'objective': 'binary:logistic',
    'max_depth': 4,
    'learning_rate': 1.0,
    'silent': 1.0,
    'n_estimators': 5
}


model = XGBClassifier(**params).fit(X_train, y_train)

y_pred = model.predict(X_test)

count_misclassified = (y_test != y_pred).sum()
print('Misclassified samples: {}'.format(count_misclassified))
accuracy = metrics.accuracy_score(y_test, y_pred)
print('Accuracy: {:.2f}'.format(accuracy))

classifier = xgb.sklearn.XGBClassifier(nthread=-1, seed=42)
classifier.fit(X_train, y_train)

plt.figure(figsize=(20,15))
xgb.plot_importance(classifier, ax=plt.gca())
plt.show()

plt.figure(figsize=(20,15))
xgb.plot_tree(classifier, ax=plt.gca())
plt.show()

print("Number of boosting trees: {}".format(classifier.n_estimators))
print("Max depth of trees: {}".format(classifier.max_depth))
print("Objective function: {}".format(classifier.objective))
