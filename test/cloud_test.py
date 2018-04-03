import BuildSimHubAPI as bsh_api

# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

# 2. start the serious coding
bsh = bsh_api.BuildSimHubAPIClient()
regular_sj = bsh.new_simulation_job()
result = regular_sj.run(file_dir, wea_dir, track=True)
# hey we are done!

if result:
    print(str(result.net_site_eui()) + " " + result.last_parameter_unit)

    load_profile = result.zone_load()
    print(load_profile)

    zl = bsh_api.postprocess.ZoneLoad(load_profile)
    print(zl.get_df())
