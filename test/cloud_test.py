import BuildSimHubAPI as bsh_api

bsh = bsh_api.BuildSimHubAPIClient()
# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

regular_sj = bsh.new_simulation_job()
response = regular_sj.run(file_dir, wea_dir, agent=1, track=True)

results = bsh.get_model(regular_sj)
print(str(results.net_site_eui()) + " " + results.last_parameter_unit)
