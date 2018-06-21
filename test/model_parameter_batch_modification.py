"""
This example file demonstrates how to:
1. upload a model to a project and run simulation on the cloud
2. batch modify a specific value under an EnergyPlus model class - e.g. watts per zone floor area under lights class
3. Run the simulation on the new model

"""

import BuildSimHubAPI as bshapi

# define models and projects
file_dir = "/Users/weilixu/Desktop/data/BaumannTestGen/smalloffice.idf"
project_api_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"

# start cloud client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
new_sj = bsh.new_simulation_job(project_api_key)

# upload and run energy model simulation
results = new_sj.create_run_model(file_dir, track=True, comment='Test parameter changes')
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)

# modify all the lights power density, and run the simulation on the modified model
new_model_api = new_sj.parameter_batch_modification('Lights', 'Watts per Zone Floor Area', value=6.2)
results = new_sj.run_model_simulation(new_model_api, unit='ip', track=True)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)
