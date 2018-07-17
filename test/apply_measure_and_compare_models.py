"""
This example demonstrates how to apply regular EEMs to a single model and do
comparison between the old model and the updated model.
"""
import BuildSimHubAPI as bshapi

# model_key can be found in each model information bar
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
model_api_key = 'f10f9365-ad6f-4f34-b4d8-e598d89af953'

bsh = bshapi.BuildSimHubAPIClient()

# step 1: get the model
model = bsh.model_results(project_api_key, model_api_key)

# step 2: apply the measure
lpd = bshapi.measures.LightLPD()
lpd.set_data(1.2)
measure = list()
measure.append(lpd)
model_api = model.apply_measures(measure)

# step 3: get the updated model
target_model = bsh.model_results(project_api_key, model_api)

# step 4: compare these two models
bsh.compare_models(model, target_model)
