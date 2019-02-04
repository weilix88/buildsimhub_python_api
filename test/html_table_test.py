
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_api_key = '48d36077-89fe-4958-9f51-27a025c530ca'
# model_key can be found in each model information bar
model_api_key = '17a01cbf-f764-44c8-8d80-4fa7959b420f'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_api_key, model_api_key)

table_data = results.html_table('Component Sizing Summary', 'Fan:OnOff')
data = pp.HTMLTable(table_data)
df = data.pandas_df()

print(data.get_cell_unit('Design Size Maximum Flow Rate', '28:MECHANICAL PTAC SUPPLY FAN'))
print(df.to_string())
