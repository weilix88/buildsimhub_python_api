"""
This sample file demonstrate three ways of running a single model simulation

"""

import BuildSimHubAPI as bsh_api

# model_key can be found in each model information bar
model_key = "39ed84d0-062b-470d-96e6-b03abff9c31c"
# project_key can be found in every project (click the information icon next to project name)
project_key = "ec4f73b5-c633-470b-91c2-8c28196a278e"

file_dir = "/Users/weilixu/Desktop/data/Webinar/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/data/Webinar/USA_CO_Golden-NREL.724666_TMY3.epw"

# initialize the client
bsh = bsh_api.BuildSimHubAPIClient()

"""
The most straightforward way to do simulation
"""
new_sj_run = bsh.new_simulation_job()
results = new_sj_run.run(file_dir, wea_dir, track=True)

if results:
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)

"""
Upload your model with a specific model_key and run simulation
"""
new_sj = bsh.new_simulation_job(model_key)
response = new_sj.create_model(file_dir)
results = new_sj.run_model_simulation(track=True)

if results:
    print(str(results.not_met_hour_cooling()) + " " + results.last_parameter_unit)
    load_data = results.zone_load()
    load = bsh_api.postprocess.ZoneLoad(load_data)
    print(load.get_df())

"""
Upload your model to a project and run simulation
"""
new_sj_project = bsh.new_simulation_job(project_key)
results = new_sj_project.create_run_model(file_dir, track=True)

if results:
    print(str(results.not_met_hour_heating()) + " " + results.last_parameter_unit)
    # results.bldg_geo()
