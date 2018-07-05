"""
This example shows how to extract parametric model information as well as their keys
The server returned data is arranged in a list - dict structure, for example:

[{'commit_msg': 'WWR: 0.4, LPD: 0.9, HeatingEff: 0.86', 'commit_date': '2018-06-20', 'commit_id': '1-146-429'},
{'commit_msg': 'WWR: 0.4, LPD: 0.9, HeatingEff: 0.8', 'commit_date': '2018-06-20', 'commit_id': '1-146-428'},
{'commit_msg': 'WWR: 0.4, LPD: 1.2, HeatingEff: 0.86', 'commit_date': '2018-06-20', 'commit_id': '1-146-427'},
{'commit_msg': 'WWR: 0.4, LPD: 1.2, HeatingEff: 0.8', 'commit_date': '2018-06-20', 'commit_id': '1-146-426'},
{'commit_msg': 'WWR: 0.6, LPD: 0.9, HeatingEff: 0.86', 'commit_date': '2018-06-20', 'commit_id': '1-146-425'}]

if there is pandas in the local python library, simply put this structure in pandas dataframe:
df = pd.DataFrame(retrieved_data)
print(df[['commit_msg', 'commit_id']])

This will rearrange the above data into a nicely pandas dataframe:
                             commit_msg  commit_id
0  WWR: 0.4, LPD: 0.9, HeatingEff: 0.86  1-146-429
1   WWR: 0.4, LPD: 0.9, HeatingEff: 0.8  1-146-428
2  WWR: 0.4, LPD: 1.2, HeatingEff: 0.86  1-146-427
3   WWR: 0.4, LPD: 1.2, HeatingEff: 0.8  1-146-426
4  WWR: 0.6, LPD: 0.9, HeatingEff: 0.86  1-146-425
5   WWR: 0.6, LPD: 0.9, HeatingEff: 0.8  1-146-424
6  WWR: 0.6, LPD: 1.2, HeatingEff: 0.86  1-146-423
7   WWR: 0.6, LPD: 1.2, HeatingEff: 0.8  1-146-422

"""

import BuildSimHubAPI as bshapi


# paste your project_api_key and model_api_key here
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = "aa09eabf-693f-4437-88cc-a522a25fba01"

bsh = bshapi.BuildSimHubAPIClient()

data_list = bsh.model_list(project_api_key, model_api_key)
print(data_list)
try:
    import pandas as pd
except:
    print("No pandas installed")

df = pd.DataFrame(data_list)

df = df[df.commit_msg != 'INIT']
print(df.to_string())

# function to reformat the model list


def post_process_models(df):
    param_list = list()
    for index, row in df.iterrows():
        msg = row['commit_msg']
        parameters = msg.split(',')
        data_dict = dict()
        for k in range(len(parameters)):
            title, val = parameters[k].split(':')
            data_dict[title.strip()] = float(val.strip())
        param_list.append(data_dict)
    parameter_df = pd.DataFrame(param_list)
    return pd.concat([df, parameter_df], axis=1)


# filter and models and extract model id
post_df = post_process_models(df)
val = post_df.loc[(post_df['HeatingEff'] == 0.88) & (post_df['LPD'] == 0.858)]['commit_id']
model_id = val.values[0]

# extract the single model eui
results = bsh.model_results(project_api_key, model_id)
print(str(results.net_site_eui()) + ' ' + results.last_parameter_unit)

