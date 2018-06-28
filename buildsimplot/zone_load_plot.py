"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT?
This script demonstrates how to zone load data in a building and how to plot the load data in a bar chart

HOW TO USE THE SCRIPT?
Replace the project_api_key and model_api_key with your model

PACKAGE REQUIRED:
Pandas, Plotly

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

"""
INPUT
"""
# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

"""
SCRIPT
"""
# initialize the client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
results = bsh.model_results(project_api_key, model_api_key)

"""
PLOT!
"""
zone_load_data = results.zone_load()
zone_level_load = pp.ZoneLoad(zone_load_data)
print(zone_level_load.pandas_df())
zone_level_load.load_bar_chart_plot('density')

