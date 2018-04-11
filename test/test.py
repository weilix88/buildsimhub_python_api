"""
8.9 test
"""

import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()
project_key = "ec4f73b5-c633-470b-91c2-8c28196a278e"

# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"
wea_dir = "/Users/weilixu/Desktop/data/jsontest/in.epw"
# 2. this is optional
# new_sj_project = bsh.new_simulation_job(project_key)
new_sj = bsh.new_simulation_job()
# 3. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers

# results = new_sj_project.create_run_model(file_dir, track=True)
results = new_sj.run(file_dir, wea_dir, track=True)
if results:
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)
    results.bldg_geo()

