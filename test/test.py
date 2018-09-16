import BuildSimHubAPI as bshapi
import pandas as pd

project_api_key = '8b7a41d1-f05a-49cd-8a58-d9ec41b00ab0'
model_api_key = '9d21ac7d-50ea-48ca-b9c0-3cee601d0834'

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

model = bsh.model_list(project_api_key, model_api_key)
