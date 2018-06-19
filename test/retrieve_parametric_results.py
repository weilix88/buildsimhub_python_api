import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp
import os
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
from plotly.offline import plot
import plotly.graph_objs as go

project_api_key = "f698ff06-4388-4549-8a29-e227dbc7b696"
model_api_key = "96cee83c-682a-4e84-972e-fc21560d4cf5"
results = bsh_api.helpers.ParametricModel(project_api_key, model_api_key)

# Collect results
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit

print(result_dict)
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

