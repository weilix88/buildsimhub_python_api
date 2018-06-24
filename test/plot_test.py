"""
This example shows how to directly retrieve the parametric
results and use plotly integration to do scatter plot and
paralle_coordinate chart plot

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

# retrieve the results from the parametric simulations
bsh = bsh_api.BuildSimHubAPIClient()
results = bsh.parametric_results(project_api_key, model_api_key)
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit

# post process the parametric results and do the plot
plot = pp.ParametricPlot(result_dict, result_unit)
print(plot.pandas_df())

# scatter plot
plot.scatter_chart_plot()
# parallel coordinate plot - no legend
plot.parallel_coordinate_plot()
# parallel coordinate plot - LPD legend
plot.parallel_coordinate_plot('LPD')

