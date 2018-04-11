"""
8.9 test
"""
import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()
project_key = "ec4f73b5-c633-470b-91c2-8c28196a278e"
model_key = "39ed84d0-062b-470d-96e6-b03abff9c31c"

# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"
wea_dir = "/Users/weilixu/Desktop/data/jsontest/in.epw"

new_sj = bsh.new_simulation_job(model_key)
response = new_sj.create_model(file_dir)
results = new_sj.run_model_simulation(track=True)
print(results.get_simulation_results('eio'))
print(results.get_simulation_results('rdd'))

if results:
    print(str(results.not_met_hour_cooling()) + " " + results.last_parameter_unit)
    load_data = results.zone_load()
    load = bshapi.postprocess.ZoneLoad(load_data)
    print(load.get_df())
