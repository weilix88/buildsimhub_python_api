import BuildSimHubAPI as bsh_api

# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/error.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

bsh = bsh_api.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job()
results = new_sj.run(file_dir, wea_dir, unit='si', track=True)

if results:
    print(str(results.net_site_eui()))
