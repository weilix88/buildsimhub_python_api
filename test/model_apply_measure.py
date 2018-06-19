import BuildSimHubAPI as bshapi

file_dir = "/Users/weilixu/Desktop/data/BaumannTestGen/smalloffice.idf"

project_api_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
new_sj = bsh.new_simulation_job(project_api_key)

results = new_sj.create_run_model(file_dir, track=True)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)

measure_list = list()
light = bshapi.measures.LightLPD()
light.set_data(6.0)
measure_list.append(light)

new_model_api = new_sj.apply_measures(measure_list)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)
