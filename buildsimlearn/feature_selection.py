"""
AUTHOR: Tracy Ruan
Date: 6/30/2018

What is this script for?
This script shows how to do the feature selection using Random Forester regressor. The importance of each feature
will be displayed in the end.

How to use this script?
Replace the project_api_key and model_api_key in this script. Make sure that the model_api_key is the one provided
after a successful parametric run.
Specify the number of trees in the forest (n_estimate)


Package required:
pandas, numpy, sci-kit learn, matplotlib

"""

import BuildSimHubAPI as bsh_api
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

"""
USER INPUT
"""
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = 'aa09eabf-693f-4437-88cc-a522a25fba01'
n_estimate = 1000

"""
SCRIPT
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
values = np.array(df['value'])

# axis 1 refers to the columns
features_old = df.drop('value', axis=1)
features = features_old.drop('model_plot', axis=1)
feature_list = list(features.columns)
features = np.array(features)
print(feature_list)

# Split the data into training and testing sets
train_features, test_features, train_values, test_values = train_test_split(features, values)

# train models
rf = RandomForestRegressor(n_estimators=n_estimate)

# feature selection
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

# variance importance plot
plt.style.use('fivethirtyeight')
# list of x locations for plotting
x_values = list(range(len(importances)))
# Make a bar chart
plt.bar(x_values, importances, orientation='vertical')
# Tick labels for x axis
plt.xticks(x_values, feature_list, rotation='vertical')
# Axis labels and title
plt.ylabel('Importance')
plt.xlabel('Variable')
plt.title('Variable Importances')
plt.show()
