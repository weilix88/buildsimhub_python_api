"""
This sample file demonstrate how to download a model from BuildSimHub using API

"""

import BuildSimHubAPI as bshapi

# project_key can be found in every project (click the information icon next to project name)
project_key = "4fee37fd-f257-4ecb-a2eb-6ef31114048c"
# model_key can be found in each model information bar
model_key = "876dcf54-42f1-4576-ab4a-be2d0f5052d7"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_key, model_key)
print(results.download_model())


