"""
Sample code to demonstrate a parametric workflow

"""

import BuildSimHubAPI as bsh_api
import pandas as pd


# 1. set your folder key
# paste your project api key
project_api_key = ''
# paste your model api key
model_api_key = ''

bsh = bsh_api.BuildSimHubAPIClient()
param_list_raw = bsh.model_list(project_api_key, model_api_key)


param_list = pd.DataFrame(param_list_raw)
print(param_list.to_string())
one_example_id = param_list['commit_id'][0]

one_model_results = bsh.model_results(project_api_key, one_example_id)
print(str(one_model_results.net_site_eui()) + " " + one_model_results.last_parameter_unit)


