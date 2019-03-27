
import BuildSimHubAPI as bshapi
import pandas as pd

# project_key can be found in every project (click the information icon next to project name)
project_api_key = '5a768d43-4b1f-46b8-806e-ab43186162a1'
# model_key can be found in each model information bar
model_api_key = 'ed10bb8c-bc4b-4fcf-b643-a0c715e9c5d9'
file_dir = '/Users/weilixu/Desktop/data/mediumoffice.idf'
wea_dif = '/Applications/EnergyPlus-8-8-0/WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
# initialize the client
bsh = bshapi.BuildSimHubAPIClient()

new_sim = bsh.new_simulation_job(project_api_key)
new_sim.run(file_dir=file_dir, unit='si', track=True)


