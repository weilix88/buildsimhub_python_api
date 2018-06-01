
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "f613129e-69c4-46fc-b1c3-ff7569d50194"
# model_key can be found in each model information bar
model_key = "e5326462-447e-4cb6-bb77-cb886b80408b"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bshapi.helpers.Model(project_key, model_key)

table_data = results.html_table('Annual Building Utility Performance Summary', 'End Uses')
data = pp.HTMLTable(table_data)
df = data.pandas_df()

data.table_bar_chart_plot(orientation='row', skip_rows=['Total End Uses'], title='End Uses', image_name='bar_table')
