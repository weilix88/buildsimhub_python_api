"""
This sample file demonstrate three ways of running a single model simulation

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"
wea_dir = "/Users/weilixu/Desktop/data/jsontest/in.epw"
# initialize the client
bsh = bsh_api.BuildSimHubAPIClient()

"""
The most straightforward way to do simulation
"""
new_sj_run = bsh.new_simulation_job(project_key)
results = new_sj_run.run(file_dir, track=True)

if results:
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)

"""
Upload your model with a specific model_key and run simulation
"""
new_sj = bsh.new_simulation_job(project_key)
response = new_sj.create_model(file_dir)
results = new_sj.run_model_simulation(track=True)

if results:
    print(str(results.not_met_hour_cooling()) + " " + results.last_parameter_unit)
    load_data = results.zone_load()
    load = pp.ZoneLoad(load_data)
    print(load.pandas_df())
