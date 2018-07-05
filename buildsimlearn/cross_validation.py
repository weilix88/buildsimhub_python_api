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
import os
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
from plotly.offline import plot
import plotly.graph_objs as go

# Parametric Study
# 1. set your folder key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

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
lr = linear_model.LinearRegression()
# default is 3 fold
predicted = cross_val_predict(lr, x, y)

trace1 = go.Scatter(x=y, y=predicted, mode='markers',
                    marker=dict(size=8,
                                color='rgb(0, 0, 255)',
                                line=dict(
                                    width=2,
                                    color='rgb(0, 0, 0)'))
                    )
trace2 = go.Scatter(x=[y.min(), y.max()], y=[y.min(), y.max()],
                    line=dict(color=('rgb(0, 0, 0)'),
                              width=5, dash='dash')
                    )
layout = go.Layout(showlegend=False,
                    yaxis=dict(
                        zeroline=False,
                        title='Predicted'),
                    xaxis=dict(
                        title='Measured', )
                    )

fig = go.Figure(data=[trace1, trace2], layout=layout)
# layout['annotations'] = annotation
dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
fig = dict(data=[trace1, trace2], layout=layout)
plot(fig, filename=dir + '/' + 'test.html')
