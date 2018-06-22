import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

project_api_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"
model_api_key = "1471ba46-2af4-4aa0-b046-e62d64900e35"

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

data_list = bsh.model_list(project_api_key, model_api_key)
model_list = pp.ModelList(data_list)
df = model_list.pandas_df()

print(df)
print(df['commit_id'])
