"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT
This script demonstrates how to retrieve two hourly data with different units
from a simulation and plot the data in line chart.

HOW TO USE THE SCRIPT
Replace the project_api_key and model_api_key with your model
Change the variable index of the target variables in the variable list.
variable_one_index
variable_two_index

PACKAGE USED:
Pandas, Plotly

"""

import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

"""
INPUT
"""
# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'
variable_one_index = 1
variable_two_index = 45

"""
SCRIPT
"""
# initialize the client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
results = bsh.model_results(project_api_key, model_api_key)

# get the list of hourly variables
variable_list = results.hourly_data()
for i in range(len(variable_list)):
    print("Index: " + str(i) + ": " + variable_list[i])
# select one variable for post processing
variable_name = variable_list[variable_one_index]

"""
PLOT!
"""
# post process use HourlyPlot class
variable_data = results.hourly_data(variable_name)
hourly_plot = pp.HourlyPlot(variable_data, variable_name)

# retrieve more hourly data and combine into one dataframe
variable_two_name = variable_list[variable_two_index]
variable_data = results.hourly_data(variable_two_name)
hourly_plot.add_column(variable_data, variable_two_name)
hourly_plot.line_chart_plot()
