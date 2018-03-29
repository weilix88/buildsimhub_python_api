import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()

# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir="/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"
# 2. this is optional
new_sj = bsh.new_simulation_job()
# 3. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers

# response = newSj.create_run_model(file_dir)
response = new_sj.run(file_dir, wea_dir, track=True)
print(response)

results = bsh.get_model(new_sj)
load_profile = results.zone_load()
print(load_profile)

zl = bshapi.postprocess.ZoneLoad(load_profile)
print(zl.get_df())
