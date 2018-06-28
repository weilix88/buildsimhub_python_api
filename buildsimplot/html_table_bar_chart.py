"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT?
This script demonstrates how to retrieve a table from HTML and plot the data in bar chart

HOW TO USE THE SCRIPT?
Replace the project_api_key and model_api_key with your model
Replace the report name - typically in the content of the HTML
Replace the table name - table name is usually above the Table in the HTML
Add row header to the skip_row: Skip row will let the plot know which rows of data should ignore in the plot
Add column header to the skip_col: Skip col will let the plot know which cols of data should ignore in the plot
plot_orientation: row or column - row uses table row as legend and column as x-axis ticks,
                and column uses table column as legend and row as x-axis ticks.
plot_title: Title of the plot

PACKAGES USED:
Pandas, Plotly

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp


"""
INPUT
"""
# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'
report = 'Annual Building Utility Performance Summary'
table = 'End Uses'
report_for = 'EntireFacility'
skip_row = ['Total End Uses']
skip_col = []
plot_orientation = 'row'
plot_title = 'End Uses'

"""
SCRIPT
"""
# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_api_key, model_api_key)

"""
PLOT!
"""
table_data = results.html_table(report, table)
data = pp.HTMLTable(table_data)
df = data.pandas_df()

data.table_bar_chart_plot(orientation=plot_orientation, skip_cols=skip_col, skip_rows=skip_row,
                          title=plot_title, image_name='bar_table')
