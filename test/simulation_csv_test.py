"""
8.9 test
"""
import BuildSimHubAPI as bshapi


bsh = bshapi.BuildSimHubAPIClient()
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# 1. define the absolute directory of your energy model
file_dir = '/Users/weilixu/Desktop/data/schedule/5ZoneTDV.idf'
wea_dir = '/Users/weilixu/Desktop/data/jsontest/in.epw'
csv_folder = '/Users/weilixu/Desktop/data/schedule/csv'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job(project_api_key)
results = new_sj.run(file_dir=file_dir, epw_dir=wea_dir, add_files=csv_folder, track=True)

if results:
    load_data = results.zone_load()
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)



