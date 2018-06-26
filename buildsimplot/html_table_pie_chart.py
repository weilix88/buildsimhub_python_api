
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_api_key, model_api_key)

table_data = results.html_table('Annual Building Utility Performance Summary', 'End Uses')
data = pp.HTMLTable(table_data)
df = data.pandas_df()

data.table_pie_chart_plot(orientation='row', skip_rows=['Total End Uses'], title='End Uses', image_name='pie_table')
