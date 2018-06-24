"""
This example shows how to upload a model with customized csv schedules

Put all the relevant schedules under one folder
and then add the folder directory to the add_files parameter.

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

bsh = bshapi.BuildSimHubAPIClient()
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'

# 1. define the absolute directory of your energy model
file_dir = '/Users/weilixu/Desktop/data/schedule/5ZoneTDV.idf'
wea_dir = "/Users/weilixu/Desktop/data/jsontest/in.epw"

new_sj = bsh.new_simulation_job(project_api_key)
results = new_sj.run(file_dir=file_dir, epw_dir=wea_dir,
                     add_files='/Users/weilixu/Desktop/data/schedule/csv', track=True)

if results:
    load_data = results.zone_load()
    print(load_data)
    zl = pp.ZoneLoad(load_data)
    print(zl.pandas_df())
