"""
AUTHOR: Weili Xu
Date: 6/30/2018

What is this script for?
This script use the parametric simulation results to train a regression model
using cross validation method.

How to use this script?
Replace the project_api_key and model_api_key in this script. Make sure that the model_api_key is the one provided
after a successful parametric run.

Package required:
sci-kit learn, plotly
"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp
from sklearn.model_selection import cross_validate
from sklearn import linear_model

# Parametric Study
# 1. set your folder key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'
# hyper-parameter
# number of folds
cv_fold = 3
# CPU use for parallelism the calculation
cpu = 1
# insert algorithms here
algs = [linear_model.LinearRegression()]

# SCRIPT
bsh = bsh_api.BuildSimHubAPIClient()
results = bsh.parametric_results(project_api_key, model_api_key)

# Collect results
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit

# Plot
param_plot = pp.ParametricPlot(result_dict, result_unit)
df = param_plot.pandas_df()

# Training code starts from here
y = df.loc[:, 'Value']
x = df.loc[:, df.columns != 'Value']
# default is 3 fold
for alg in algs:
    train_result = cross_validate(alg, x, y, cv=cv_fold, n_jobs=cpu, return_train_score=False)
    print(train_result['test_score'])
