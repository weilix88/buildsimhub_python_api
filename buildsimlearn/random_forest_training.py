"""
AUTHOR: Tracy Ruan
Date: 6/30/2018

What is this script for?
This script extract results from a parametric study from BuildSimCloud, and then use the results to train a random
forest tree model. The training accuracy will be demonstrated by MAE and MAPE, and predicted vs. actual plot will be
used for comparison.

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
User Input
"""
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = 'aa09eabf-693f-4437-88cc-a522a25fba01'
# The number of trees in the forest.
n_estimate = 1000

"""
Script
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
rf.fit(train_features, train_values)

# predict values using rf on test data
predictions = rf.predict(test_features)
# Calculate the absolute errors
errors = abs(predictions - test_values)
# mean absolute error (MAE) is a measure of difference between two continuous variables
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

# Determine Performance Metrics
# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / test_values)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

# Actual value VS predicted value plot
plt.scatter(test_values, predictions, s=1)
plt.plot([min(test_values), max(test_values)], [min(predictions), max(predictions)], 'red', linewidth=1)
plt.ylabel('Actual Value')
plt.xlabel('Predicted Value')
plt.title('Actual VS Predicted')
plt.show()
