# Use pandas to load the data in a dataFrame
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# load data
df = pd.read_excel('input/PKS1921-293-145-mjds.xls', header=1, index_col=0)

print(df.head())
print(df.shape)

y = df["S"]
X = df[[col for col in df.columns if col!='S']]
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.25, random_state=42)

print("Size of train dataset: {} rows".format(X_train.shape[0]))
print("Size of test dataset: {} rows".format(X_test.shape[0]))

classifier = xgb.sklearn.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                                       colsample_bytree=0.90, gamma=0.2, learning_rate=0.1, max_delta_step=0, max_depth=3, min_child_weight=1, missing=None, n_estimators=1000, n_jobs=1, nthread=-1, objective='multi:softprob', random_state=0, reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=42, silent=True, subsample=1)

classifier.fit(X_train, y_train)

predictions = classifier.predict(X_test)

print(pd.DataFrame(predictions, index=X_test.index, columns=['Predicted default']).head())

print(pd.DataFrame(y_test).head())

print("Number of boosting trees: {}".format(classifier.n_estimators))
print("Max depth of trees: {}".format(classifier.max_depth))
print("Objective function: {}".format(classifier.objective))

# evaluate predictions
accuracy = 100. * classifier.score(X_test, y_test)
print("Model Accuracy: ".format(accuracy))

# Graphics
plt.figure(figsize=(20,15))
xgb.plot_importance(classifier, ax=plt.gca())
plt.show()

plt.figure(figsize=(20,15))
xgb.plot_tree(classifier, ax=plt.gca())
plt.show()


