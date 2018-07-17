"""
This example demonstrate how to get a list of zones in a model.

"""
import BuildSimHubAPI as bshapi

# model_key can be found in each model information bar
# paste your model api key
global_project_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = 'f10f9365-ad6f-4f34-b4d8-e598d89af953'

bsh = bshapi.BuildSimHubAPIClient()

model = bsh.model_results(global_project_key, model_api_key)
print(model.zone_list())
