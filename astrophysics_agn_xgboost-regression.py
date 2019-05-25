import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold

train = pd.read_csv('input/PKS1921-293-145-train.csv')
test=pd.read_csv('input/PKS1921-293-145-test.csv')
train_num = train.shape[0]
data = pd.concat([train,test])

train = data[:train_num]
test = data[train_num:]

y_train = train["S"].values
X_train = train.drop("Peak",axis=1).values
y_test = test["S"].values
X_test =test.drop("Peak",axis=1).values

gbm = xgb.XGBRegressor()
reg_cv = GridSearchCV(gbm, {"colsample_bytree":[1.0],"min_child_weight":[1.0,1.2]
                            ,'max_depth': [3,4,6], 'n_estimators': [500,1000]}, verbose=1)
reg_cv.fit(X_train,y_train)

gbm = xgb.XGBRegressor(reg_cv.best_params)
gbm.fit(X_train,y_train)

pre = gbm.predict(X_test)

gbm.score(X_test,y_test)
gbm.score(X_train,y_train)

