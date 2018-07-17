"""
This example shows how to extract model information under a project as well as their keys
The server returned data is arranged in a list - dict structure, for example:

[{'branch_name': '5zoneaircooled_uniformloading.epjson', 'branch_id': 146, 'branch_type': 'idf',
'branch_description': '5zoneaircooled_uniformloading.epjson parametric',
'api_key': '1471ba46-2af4-4aa0-e62d64900e35','last_modified_time': '2018-06-20 14:52:24'},
{'branch_name': 'Python API', 'branch_id': 145, 'branch_type': 'idf',
'branch_description': 'Python API', 'api_key': '388a62f2-123f-40b2-5aa67dd8e154',
'last_modified_time': '2018-06-20 14:07:07'}]

if there is pandas in the local python library, simply put this structure in pandas dataframe:
df = pd.DataFrame(retrieved_data)
print(df)

This will rearrange the above data into a nicely pandas dataframe:
                                           branch_name                          api_key
0                 5zoneaircooled_uniformloading.epjson  1471ba46-2af4-4aa0-e62d64900e35
1                                           Python API  388a62f2-123f-40b2-5aa67dd8e154
2                               Test parameter changes  6db446a8-11ae-40c9-0a3e0eaffba8
3                                           Python API  08aea646-100e-4b4e-cbb74e60948a

"""
import BuildSimHubAPI as bshapi

project_api_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"

bsh = bshapi.BuildSimHubAPIClient()

project_list = bsh.project_model_list(project_api_key)
try:
    import pandas as pd
except:
    print("No pandas installed")

df = pd.DataFrame(project_list)
print(df.to_string())
# print(df[''])
