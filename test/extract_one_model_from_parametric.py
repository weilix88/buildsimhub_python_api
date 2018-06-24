"""
This sample code demonstrates how to extract a single model from a parametric run

"""

import BuildSimHubAPI as bsh_api
import pandas as pd


# 1. set your folder key
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

bsh = bsh_api.BuildSimHubAPIClient()
param_list_raw = bsh.model_list(project_api_key, model_api_key)


param_list = pd.DataFrame(param_list_raw)
print(param_list.to_string())
one_example_id = param_list['commit_id'][0]

one_model_results = bsh.model_results(project_api_key, one_example_id)
print(str(one_model_results.net_site_eui()) + " " + one_model_results.last_parameter_unit)


