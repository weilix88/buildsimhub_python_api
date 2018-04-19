"""
8.9 test
"""
import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()
project_key = "ad7e830f-b555-497c-ba22-c7949289a1ac"
model_key = "39ed84d0-062b-470d-96e6-b03abff9c31c"

# 1. define the absolute directory of your energy model
#file_dir = ["/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON",
#            "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled.idf",
#            "/Users/weilixu/Desktop/data/jsontest/130NF.idf"]

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled.idf"

wea_dir = "/Users/weilixu/Desktop/data/jsontest/in.epw"

new_sj = bsh.new_simulation_job(project_key)
results = new_sj.run(file_dir, wea_dir, track=True)

if results:
    load_data = results.zone_load('SPACE1-1')
    # print(load_data)
    print(results.get_simulation_results('err'))
# if results:
#    print(str(results.not_met_hour_cooling()) + " " + results.last_parameter_unit)
#    load_data = results.zone_load()
#    load = bshapi.postprocess.ZoneLoad(load_data)
#    print(load.get_df())
