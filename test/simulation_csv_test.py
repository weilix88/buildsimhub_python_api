"""
8.9 test
"""
import BuildSimHubAPI as bshapi


bsh = bshapi.BuildSimHubAPIClient()
project_key = 'f613129e-69c4-46fc-b1c3-ff7569d50194'
# 1. define the absolute directory of your energy model
file_dir = '/Users/weilixu/Desktop/data/schedule/5ZoneTDV.idf'
wea_dir = '/Users/weilixu/Desktop/data/jsontest/in.epw'
csv_folder = '/Users/weilixu/Desktop/data/schedule/csv'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job(project_key)
results = new_sj.run(file_dir=file_dir, epw_dir=wea_dir, add_files=csv_folder, track=True)

if results:
    load_data = results.zone_load()
    print(str(results.net_site_eui()) + " " + results.last_parameter_unit)



