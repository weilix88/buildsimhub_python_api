"""
This example file demonstrates how to:
1. upload a model to a project and run simulation on the cloud
2. Apply energy efficient measure to the uploaded model - a new model will created under the same model api key
3. Run the simulation on the new model

It should be noted that only set_data() is available for applying energy efficient measures to a single model.
If the user wish to run parametric, then parametric_test.py contains the relevant example.

"""
import BuildSimHubAPI as bshapi

# define models and projects
file_dir = "/Users/weilixu/Desktop/data/smalloffice.idf"
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'

# start cloud client
bsh = bshapi.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job(project_api_key)
# upload and run the model under a project.
results = new_sj.create_run_model(file_dir, track=True)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)

# add light power density measure the list
measure_list = list()
light = bshapi.measures.LightLPD()
light.set_data(6.0)
measure_list.append(light)

# apply measure - you will get a new model key (e.g.: 1-11-111), rerun the new model
new_model_api = new_sj.apply_measures(measure_list)
results = new_sj.run_model_simulation(new_model_api, unit='ip', track=True)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)
