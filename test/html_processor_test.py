"""
This example demonstrates how to use the HTML parser in BuildSimHub API library
"""

import BuildSimHubAPI as bshapi

# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

report = "Annual Building Utility Performance Summary"
table = "Site and Source Energy "
row_name = "Net Site Energy"
column_name = "Total Energy"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_api_key, model_api_key)

html = results.get_simulation_results('html')

# to save the html in your local directory
# bshapi.htmlParser.save_html(html, 'YOUR LOCAL DIRECTORY')
net_total_eui = bshapi.htmlParser.extract_value_from_table(html, report, table, column_name, row_name)
print(net_total_eui)
