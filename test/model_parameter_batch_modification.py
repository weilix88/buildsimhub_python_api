import BuildSimHubAPI as bshapi

file_dir = "/Users/weilixu/Desktop/data/BaumannTestGen/smalloffice.idf"

project_api_key = "f698ff06-4388-4549-8a29-e227dbc7b696"

bsh = bshapi.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job(project_api_key)

results = new_sj.create_run_model(file_dir, track=True)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)

new_model_api = new_sj.parameter_batch_modification('Lights', 'Watts per Zone Floor Area', value=6.2)
results = new_sj.run_model_simulation(new_model_api, unit='si', track=True)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)
