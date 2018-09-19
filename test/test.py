"""
This provides a sample workflow to kick-off a parametric study using the brute force algorithm
The brute force algorithm will exhaustively simulate all the possible combinations of the
measures -

e.g.
if:
 2 options for lighting power density,
 2 options for window wall ratio,
 2 options for heating efficiency

The total number of possible combinations is 2 x 2 x 2 = 8 - so this script will run 8 simulations.

Enter the project_api_key - which link to the project that you wish to host your parametric study.

Enter the model_api_key if you wish to use a model on the BuildSim Cloud as seed model,
or you can specify local_file_dir variable to submit a seed model (you need to switch the model_api_key to None or ''
in order to submit the model from local).

"""

import BuildSimHubAPI as bsh_api

# 1. set your folder key
project_api_key = 'faa5ac84-6f72-427c-a4e7-278e9c17830d'
model_api_key = 'b38e3623-7a19-49c6-9344-0256761d1c4a'
local_file_dir = ''

bsh = bsh_api.BuildSimHubAPIClient()
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
new_pj = bsh.new_parametric_job(project_api_key)
measure_list = list()
# Define EEMs

# inf = bsh_api.measures.Infiltration()
# inf_ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
# inf.set_datalist(inf_ratio)
# measure_list.append(inf)

heff = bsh_api.measures.HeatingDXEfficiency()
h_cop = [2.93, 3.28]
heff.set_datalist(h_cop)
measure_list.append(heff)

# wwr = bsh_api.measures.WindowWallRatio()
# wwr_ratio = [0.6, 0.4]
# wwr.set_datalist(wwr_ratio)
# measure_list.append(wwr)

# lpd = bsh_api.measures.LightLPD('ip')
# lpdValue = [1.2, 0.9]
# lpd.set_datalist(lpdValue)
# measure_list.append(lpd)

# heatEff = bsh_api.measures.HeatingEfficiency()
# cop = [0.8, 0.86, 0.9]
# heatEff.set_datalist(cop)
# measure_list.append(heatEff)

# Add EEMs to parametric job
new_pj.add_model_measures(measure_list)

# Start!
if model_api_key is not None and model_api_key != '':
    results = new_pj.submit_parametric_study(model_api_key=model_api_key, track=True)
elif local_file_dir is not None and local_file_dir != '':
    results = new_pj.submit_parametric_study_local(local_file_dir, track=True)
