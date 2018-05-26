"""
This sample file demonstrate how to download a model from BuildSimHub using API

"""

import BuildSimHubAPI as bshapi

# project_key can be found in every project (click the information icon next to project name)
project_key = "f613129e-69c4-46fc-b1c3-ff7569d50194"
# model_key can be found in each model information bar
model_key = "e5326462-447e-4cb6-bb77-cb886b80408b"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bshapi.helpers.Model(project_key, model_key)
print(results.download_model(model_key))


