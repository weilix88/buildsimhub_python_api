"""
This example demonstrates the mapping of parametric case number and parametric commit_id

The parametric model list
   commit_date  commit_id                               commit_msg
0   2018-06-24  1-339-751  WWR: 0.42, LPD: 0.858, HeatingEff: 0.88
1   2018-06-24  1-339-750  WWR: 0.58, LPD: 1.158, HeatingEff: 0.89

The parametric results returns a dataframe:
     case                               commit_msg  value
0   case1  WWR: 0.42, LPD: 0.858, HeatingEff: 0.88  17.83
1   case2  WWR: 0.58, LPD: 1.158, HeatingEff: 0.89  20.63

After merged:
     case                               commit_msg  value commit_date  commit_id
0   case1  WWR: 0.42, LPD: 0.858, HeatingEff: 0.88  17.83  2018-06-24  1-339-751
1   case2  WWR: 0.58, LPD: 1.158, HeatingEff: 0.89  20.63  2018-06-24  1-339-750

Replace the project api key and model api key to run this script.
"""

import BuildSimHubAPI as bshapi
import pandas as pd

# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

bsh = bshapi.BuildSimHubAPIClient()

parametric_results = bsh.parametric_results(project_api_key, model_api_key)
variable = parametric_results.net_site_eui()

length = len(variable['value'])
data_list = list()

for index in range(length):
    data_dict = dict()
    data_dict['value'] = variable['value'][index]
    data_dict['commit_msg'] = variable['model'][index]
    data_dict['case'] = variable['model_plot'][index]
    data_list.append(data_dict)

param_output = pd.DataFrame(data_list)
param_list_raw = bsh.model_list(project_api_key, model_api_key)
param_list = pd.DataFrame(param_list_raw)
print(param_list.to_string())
print(param_output.to_string())

merged_df = pd.merge(param_output, param_list, on="commit_msg")
print(merged_df.to_string())
