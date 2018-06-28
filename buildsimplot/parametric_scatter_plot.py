"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT?
This script demonstrates how to retrieve the parametric data and plot scatter plot

HOW TO USE THE SCRIPT?
Replace the project_api_key and model_api_key with your model

PACKAGE REQUIRED:
Pandas, Plotly

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

"""
INPUT
"""
# 1. set your folder key
project_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = 'aa09eabf-693f-4437-88cc-a522a25fba01'

"""
SCRIPT
"""
bsh = bsh_api.BuildSimHubAPIClient()
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
results = bsh.parametric_results(project_key, model_api_key)

# Collect results
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit


"""
PLOT!
"""
# Plot
plot = pp.ParametricPlot(result_dict, result_unit)
print(plot.pandas_df())
plot.scatter_chart_plot("Scatter plot demo")
