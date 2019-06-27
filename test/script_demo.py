
import BuildSimHubAPI as bshapi
import pandas as pd

# project_key can be found in every project (click the information icon next to project name)
project_api_key = '103ead80-bcd6-4ea0-96ad-7f042d8d3340'
# model_key can be found in each model information bar
model_api_key = '003c7efa-1c75-43c9-bca3-0d0253c32783'
file_dir = '/Users/weilixu/Desktop/data/mediumoffice.idf'
wea_dif = '/Applications/EnergyPlus-8-8-0/WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
# initialize the client
bsh = bshapi.BuildSimHubAPIClient()

new_model = bsh.model_results(project_api_key, model_api_key)
light = new_model.class_template('Lights')
print(light)
