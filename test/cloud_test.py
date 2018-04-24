"""
This sample file demonstrate three ways of running a single model simulation

"""

import BuildSimHubAPI as bsh_api

# model_key can be found in each model information bar
model_key = "96d21c84-d17f-41a2-9da4-1d09ca43736e"
# project_key can be found in every project (click the information icon next to project name)
project_key = "d43f2d17-7da6-4fd1-800c-62651001d453"

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"
wea_dir = "/Users/weilixu/Desktop/data/jsontest/in.epw"
# initialize the client
bsh = bsh_api.BuildSimHubAPIClient()
"""
The most straightforward way to do simulation
"""
new_sj_run = bsh.new_simulation_job(project_key)
results = new_sj_run.run(file_dir, wea_dir, track=True)

if results:
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)

"""
Upload your model to a project and run simulation
"""
new_sj_project = bsh.new_simulation_job(project_key)
results = new_sj_project.create_run_model(file_dir, track=True)
if results:
    print(str(results.not_met_hour_heating()) + " " + results.last_parameter_unit)
    results.bldg_geo()

"""
Upload your model with a specific model_key and run simulation
"""
new_sj = bsh.new_simulation_job(project_key)
response = new_sj.create_model(file_dir)
results = new_sj.run_model_simulation(track=True)

if results:
    print(str(results.not_met_hour_cooling()) + " " + results.last_parameter_unit)
    load_data = results.zone_load()
    load = bsh_api.postprocess.ZoneLoad(load_data)
    print(load.get_df())
