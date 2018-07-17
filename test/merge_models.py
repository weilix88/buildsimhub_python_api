"""
This example demonstrate how to merge two models through API.
"""
import BuildSimHubAPI as bshapi


# model_key can be found in each model information bar
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
updated_model_id = '1-559-1480'
compare_model_id = '1-559-1441'

bsh = bshapi.BuildSimHubAPIClient()

# get the two models
updated_model = bsh.model_results(project_api_key, updated_model_id)
compare_model = bsh.model_results(project_api_key, compare_model_id)

# merge models
bsh.merge_models(updated_model, compare_model)
