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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

"""
USER INPUT
"""
project_api_key = 'ec9ea39e-4c2a-47e3-baf2-c42a1a8210fa'
model_api_key = '453b2cf5-c443-40a3-84b6-30f4f5ab087a'

"""
SCRIPT!!
"""
bsh = bsh_api.BuildSimHubAPIClient()
results = bsh.parametric_results(project_api_key, model_api_key)
# Collect results
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit

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

print('description for each feature: ')
print(df_copy.describe(include='all'))

values = np.array(df_copy['value'])
# axis 1 refers to the column
features = df_copy.drop('value', axis=1)
feature_list = list(features.columns)
features = np.array(features)

# linear regression model
X_train, X_test, y_train, y_test = train_test_split(features, values, test_size=0.2)
print('X_train: ' + str(X_train.shape))
print('X_test: ' + str(X_test.shape))
print('y_train: ' + str(y_train.shape))
print('y_test:' + str(y_test.shape))

print('Correlation Plot: ')
plt.matshow(df_copy.corr())
plt.xticks(range(len(df_copy.columns)), df_copy.columns)
plt.yticks(range(len(df_copy.columns)), df_copy.columns)
plt.colorbar()


print('Correlation Table: ')
corr = df_copy.corr()
print(corr)
plt.show()


# train the model
lm = LinearRegression()
lm.fit(X_train, y_train)
print('Interpret value β0: '+str(lm.intercept_))

print('training score: ' + str(lm.score(X_train, y_train)))
print('testing score: ' + str(lm.score(X_test, y_test)))

print('Coefficient value for each feature: ')
coeff_df = pd.DataFrame(list(zip(feature_list, lm.coef_)), columns=['features', 'estimated coeficients'])
print(coeff_df)


# make predictions and view output comparison table
prediction = lm.predict(X_test)
pred_df = pd.DataFrame({'Actual': y_test, 'Predicted': prediction})
pred_df.head(4)


# A helper method for pretty-printing linear models
def pretty_print_linear(coefs, names=None, sort=False):
    if names is None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)
    if sort:
        lst = sorted(lst, key=lambda x: -np.abs(x[0]))
    return " + ".join("%s * %s" % (round(coef, 3), name)
                      for coef, name in lst)


print('Linear regression model: ' + str(lm.intercept_) + ' + ' + pretty_print_linear(lm.coef_))

# evaluate model perfomance
from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, prediction))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, prediction))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, prediction)))