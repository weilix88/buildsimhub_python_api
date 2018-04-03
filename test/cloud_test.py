import BuildSimHubAPI as bsh_api

# 1. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/error.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

# 2. start the serious coding
bsh = bsh_api.BuildSimHubAPIClient()
regular_sj = bsh.new_simulation_job()
response = regular_sj.run(file_dir, wea_dir, track=True)
# hey we are done!

if response:
    results = bsh.get_model(regular_sj)
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)

    load_profile = results.zone_load()
    print(load_profile)

    zl = bsh_api.postprocess.ZoneLoad(load_profile)
    print(zl.get_df())
