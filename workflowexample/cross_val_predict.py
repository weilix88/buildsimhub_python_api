"""
This example shows how to use scikit-learn
with BuildSimHub parametric study object
to train a regression model

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
project_key = 'f698ff06-4388-4549-8a29-e227dbc7b696'
model_key = '6ea4361d-5f8f-4f66-99e7-f0a4bb16be5b'

bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_key, model_key)

# Define EEMs
wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.6, 0.4, 0.2]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2, 0.9, 0.6]
lpd.set_datalist(lpdValue)

heatEff = bsh_api.measures.HeatingEfficiency()
eff = [0.8, 0.86, 0.92]
heatEff.set_datalist(eff)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(heatEff)

# Start!
results = new_pj.submit_parametric_study(track=True)
# results = bsh_api.helpers.ParametricModel(project_key, model_key)
if results:

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
