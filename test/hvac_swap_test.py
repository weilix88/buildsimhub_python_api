import BuildSimHubAPI as bshapi

# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'c39dceed-242b-4ea3-9fd4-e2076f89c29b'
# model_key can be found in each model information bar
model_api_key = '9e699206-3ee4-48e4-b80a-d9d103ce23ef'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_api_key, model_api_key)
id = results.hvac_swap('/Users/weilixu/Desktop/doasvrf.idf')

sim_update = bsh.new_simulation_job(project_api_key)
update_model = sim_update.run_model_simulation(id, track=True)
print(update_model.net_site_eui())
