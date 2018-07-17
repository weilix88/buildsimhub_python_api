"""
This example demonstrate how to copy one model inside a project through API.
"""
import BuildSimHubAPI as bshapi


# model_key can be found in each model information bar
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
model_api_key = 'ee6ca984-c9a4-4a5e-be08-4f7f10cb7b21'

bsh = bshapi.BuildSimHubAPIClient()

# get the two models
model = bsh.model_results(project_api_key, model_api_key)

# copy model
copied_model_id = bsh.copy_model(model)
print(copied_model_id)
