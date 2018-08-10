"""

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp
import pandas as pd

# model_key can be found in each model information bar
# paste your project api key
project_api_key = ''
# paste your model api key
model_api_key = ''

bsh = bshapi.BuildSimHubAPIClient()
models = bsh.model_list(project_api_key, model_api_key)

for model in models:
    commit_msg = model['commit_msg'].split(',')
    if len(commit_msg) > 1:
        for msg in commit_msg:
            key, val = msg.split(':')
            if key not in model:
                key = key.strip()
                model[key] = float(val)
    model.pop('commit_msg')

param_df = pd.DataFrame(models)
print(param_df)
# It should be the first one of the row
# fill in your own filtering criteria - more examples can be found here:
# https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/
target_commit_id = param_df.loc[(param_df['Roof_R'] == 29.071) & (param_df['Window_SHGC_East'] == 0.21)]['commit_id'][1]
source_commit_id = param_df.loc[(param_df['Roof_R'] == 33.422)]['commit_id'][1]

target_model = bsh.model_results(project_api_key, target_commit_id)
source_model = bsh.model_results(project_api_key, source_commit_id)

bsh.compare_models(source_model, target_model)






