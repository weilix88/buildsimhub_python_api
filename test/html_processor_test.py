"""
This example demonstrates how to use the HTML parser in BuildSimHub API library
"""

import BuildSimHubAPI as bshapi

# project_key can be found in every project (click the information icon next to project name)
project_key = "f613129e-69c4-46fc-b1c3-ff7569d50194"
# model_key can be found in each model information bar
model_key = "e5326462-447e-4cb6-bb77-cb886b80408b"

report = "Annual Building Utility Performance Summary"
table = "Site and Source Energy "
row_name = "Net Site Energy"
column_name = "Total Energy"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bshapi.helpers.Model(project_key, model_key)

html = results.get_simulation_results('html')
net_total_eui = bshapi.htmlParser.extract_value_from_table(html, report, table, column_name, row_name)
print(net_total_eui)
