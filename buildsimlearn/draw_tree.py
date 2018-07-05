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
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import pydot

"""
USER INPUT
"""
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = 'aa09eabf-693f-4437-88cc-a522a25fba01'
n_estimators = 10
max_depth = 4


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
values = np.array(df['value'])

# axis 1 refers to the columns
features_old = df.drop('value', axis=1)
features = features_old.drop('model_plot', axis=1)
feature_list = list(features.columns)
features = np.array(features)
print(feature_list)

# Split the data into training and testing sets
train_features, test_features, train_values, test_values = train_test_split(features, values)

# draw Limit depth of tree to 4 levels
rf_small = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
rf_small.fit(train_features, train_values)
# Extract the small tree
tree_small = rf_small.estimators_[5]
# Save the tree as a png image
export_graphviz(tree_small, out_file='sample_tree.dot', feature_names=feature_list, rounded=True,
                precision=1)
(graph, ) = pydot.graph_from_dot_file('sample_tree.dot')
graph.write_png('sample_tree.png')
