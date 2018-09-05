"""
AUTHOR: Tracy Ruan
Date: 6/30/2018

What is this script for?
This script can draw a decision tree based on the trained model.

How to use this script?
Replace the project_api_key and model_api_key in this script. Make sure that the model_api_key is the one provided
after a successful parametric run.
Specify the number of trees in the forest (n_estimate)
Specify the depth of the tree that you wish to draw

Package required:
pandas, numpy, sci-kit learn, pydot
It should be noted that in order to ensure pydot can correctly find the file, user
should install graphviz on their local computer.
For mac user: brew install graphviz
For linux user: sudo apt-get install graphviz
For windows user: download graphviz from here http://www.graphviz.org/download/ and
added C:\Program Files (x86)\Graphviz2.38\bin to PATH

"""

import BuildSimHubAPI as bsh_api
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import learning_curve

"""
User Inputs
"""
project_api_key = 'ec9ea39e-4c2a-47e3-baf2-c42a1a8210fa'
model_api_key = '453b2cf5-c443-40a3-84b6-30f4f5ab087a'

# User Input hyper-parameters
test_size = 0.2
C = 10
lw = 1
gamma_num = 0.05

"""
SCRIPT!!
"""

bsh = bsh_api.BuildSimHubAPIClient()
results = bsh.parametric_results(project_api_key, model_api_key)
# Collect results
result_dict = results.net_site_eui()

for i in range(len(result_dict)):
    tempstr = result_dict["value"]

dict = {}
for key in result_dict:
    if key == "model":
        templist = result_dict[key]
        tempdict = {}
        for i in range(len(templist)):
            tempstr = result_dict["model"][i]
            templist = tempstr.split(',')
            for j in range(len(templist)):
                pair = templist[j].split(': ')
                if pair[0] not in tempdict:
                    tempdict[pair[0]] = []
                tempdict[pair[0]].append(pair[1])
        for subkey in tempdict:
            dict[subkey] = tempdict[subkey]
    else:
        dict[key] = result_dict[key]

df = pd.DataFrame(dict)
df.head(5)

df_copy = df.copy()
df_copy = df_copy.drop('model_plot', axis=1).astype(float)

print(df_copy.describe(include='all'))
# print(df_copy.describe())
values= np.array(df_copy['value'])
features = df_copy.drop('value', axis = 1) # axis 1 refers to the columns
feature_list = list(features.columns)
features = np.array(features)

# SVM model
X_train, X_test, y_train, y_test = train_test_split(features, values, test_size=test_size)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# SVM linear kernel model
svr_lin = SVR(kernel='linear', C=C)
pred_lin = svr_lin.fit(X_train, y_train).predict(X_test)
# plt.plot(y_test, pred_lin)
plt.scatter(y_test, pred_lin, label='Linear model')
# change the size (hyperparameters)
plt.plot([min(y_test), max(y_test)], [min(pred_lin), max(pred_lin)], "orange", lw)
print('linear model R-squared = {}'.format(round(float(svr_lin.score(X_test, y_test)), 4)))
print('linear MSE = {}'.format(round(float(mean_squared_error(y_test, pred_lin)), 4)))

# SVM rbf kernel model
svr_rbf = SVR(kernel='rbf', C=C, gamma=gamma_num)
pred_rbf = svr_rbf.fit(X_train, y_train).predict(X_test)
plt.scatter(y_test, pred_rbf, label='rbf model')
plt.plot([min(y_test), max(y_test)], [min(pred_rbf), max(pred_rbf)], "lightblue", lw=1)
plt.xlabel("True value")
plt.ylabel("Predicted value")
plt.legend()
print('rbf model R-squared = {}'.format(round(float(svr_rbf.score(X_test, y_test)), 4)))
print('rbf model MSE = {}'.format(round(float(mean_squared_error(y_test, pred_rbf)), 4)))

plt.figure()

# features importance for linear kerner in SVM
svm = svr_lin.fit(X_train, y_train)


def f_importances(coef, names):
    imp = coef
    imp, names = zip(*sorted(zip(imp,names)))
    plt.barh(range(len(names)), imp, align='center')
    plt.yticks(range(len(names)), names)
    plt.show()


f_importances(svm.coef_[0], feature_list)

print('Coefficients:{0}, intercept {1}'.format(svm.coef_, svm.intercept_))
print('Score: {0}' .format(svm.score(X_test, y_test)) + ', which is a bit low.')

plt.figure()

# evaluate linear model perfomance
print('SVR linear Mean Absolute Error:', metrics.mean_absolute_error(y_test, pred_lin))
print('SVR linear Mean Squared Error:', metrics.mean_squared_error(y_test, pred_lin))
print('SVR linear Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, pred_lin)))

# evaluate rbf model performance
print('SVR rbf Mean Absolute Error:', metrics.mean_absolute_error(y_test, pred_rbf))
print('SVR rbf Mean Squared Error:', metrics.mean_squared_error(y_test, pred_rbf))
print('SVR rbf Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, pred_rbf)))

print('The the difference between RMSE and MAE is small, so the error size is relatively consistent.')

# We can use the function learning_curve to generate the values that are required to plot such a
# learning curve (number of samples that have been used, the average scores on the training sets
# and the average scores on the validation sets)
svr_rbf = SVR(kernel='rbf', C=C, gamma=gamma_num)
pred_rbf = svr_rbf.fit(X_train, y_train).predict(X_test)
plt.xlabel("True value")
plt.ylabel("Predicted value")
print('SVR brf R-squared = {}'.format(round(float(svr_rbf.score(X_test, y_test)), 4)))
print('SVR brf MSE = {}'.format(round(float(mean_squared_error(y_test, pred_rbf)), 4)))

svr = SVR(kernel='rbf', gamma=0.1)
train_sizes, train_scores_svr, test_scores_svr = learning_curve(svr, X_train, y_train,
                                                                train_sizes=np.linspace(0.1, 1, 10),
                                                                scoring="neg_mean_squared_error", cv=5)

svr2 = SVR(kernel='linear')
train_sizes2, train_scores_svr2, test_scores_svr2 = learning_curve(svr2, X_train, y_train,
                                                                   train_sizes=np.linspace(0.1, 1, 10),
                                                                   scoring="neg_mean_squared_error", cv=5)

plt.plot(train_sizes, -test_scores_svr.mean(1), 'o-', color="r",
         label="SVR rbf testing error")
plt.plot(train_sizes, -train_scores_svr.mean(1), 'o-', color="b",
         label="SVR rbf training error")
plt.plot(train_sizes2, -test_scores_svr2.mean(1), 'o-', color="g",
         label="SVR linear testing error")
plt.plot(train_sizes2, -train_scores_svr2.mean(1), 'o-', color="y",
         label="SVR linear training error")

plt.xlabel("Train size")
plt.ylabel("Mean Squared Error")
plt.title('Learning curves')
plt.legend(loc="best")

print('From the graph, we can know lots of information. SVR linear model has relatively low bias, '
      'compared to SVR rbf model, which indicates the model fits training data very well. '
      'The SVR linear model has lower variance, which indicates that our model prediction '
      'and true data are homogenous, which is pretty good, but on the other hand, '
      'it is possible for the model to be a bit underfitted. Both models has their advantages in our case, '
      'but after trade-off, we might prefer linear model')
plt.show()
