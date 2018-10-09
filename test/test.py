"""
This provides a sample workflow to kick-off a parametric study using the latin hypercube sampling method.
The sampling method randomly draw sample from the defined range for each parameter.
The number_of_simulation defines the number of simulations will performed in the parametric study.

Enter the project_api_key - which link to the project that you wish to host your parametric study.

Enter the model_api_key if you wish to use a model on the BuildSim Cloud as seed model,
or you can specify local_file_dir variable to submit a seed model (you need to switch the model_api_key to None or ''
in order to submit the model from local).

"""

import BuildSimHubAPI as bsh_api

# 1. set your folder key
project_key = '6e318bd2-db50-4c16-b364-5e4a8d6c81eb'
model_api_key = ''
local_file_dir = "/Users/weilixu/Desktop/data/mediumoffice.idf"
wea_dir = '/Applications/EnergyPlus-8-9-0/WeatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw'
number_of_simulation = 10

bsh = bsh_api.BuildSimHubAPIClient()
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
new_pj = bsh.new_parametric_job(project_key)

# Define EEMs
measure_list = list()

wwrn = bsh_api.measures.WindowWallRatio(orientation="N")
wwrn.set_min(0.3)
wwrn.set_max(0.6)
measure_list.append(wwrn)

wwrs = bsh_api.measures.WindowWallRatio(orientation="S")
wwrs.set_min(0.3)
wwrs.set_max(0.6)
measure_list.append(wwrs)

wwrw = bsh_api.measures.WindowWallRatio(orientation="W")
wwrw.set_min(0.3)
wwrw.set_max(0.6)
measure_list.append(wwrw)

wwre = bsh_api.measures.WindowWallRatio(orientation="E")
wwre.set_min(0.3)
wwre.set_max(0.6)
measure_list.append(wwre)

wallr = bsh_api.measures.WallRValue('ip')
wallr.set_min(20)
wallr.set_max(40)
measure_list.append(wallr)

roofr = bsh_api.measures.RoofRValue('ip')
roofr.set_min(20)
roofr.set_max(50)
measure_list.append(roofr)

overhangs = bsh_api.measures.ShadeOverhang(orientation='s')
overhangs.set_min(0)
overhangs.set_max(3.0)
measure_list.append(overhangs)

overhangn = bsh_api.measures.ShadeOverhang(orientation='n')
overhangn.set_min(0)
overhangn.set_max(3.0)
measure_list.append(overhangn)

overhange = bsh_api.measures.ShadeOverhang(orientation='e')
overhange.set_min(0)
overhange.set_max(3.0)
measure_list.append(overhange)

overhangw = bsh_api.measures.ShadeOverhang(orientation='w')
overhangw.set_min(0)
overhangw.set_max(3.0)
measure_list.append(overhangw)

fins = bsh_api.measures.ShadeFin(orientation='s')
fins.set_min(0)
fins.set_max(3.0)
measure_list.append(fins)

finn = bsh_api.measures.ShadeFin(orientation='n')
finn.set_min(0)
finn.set_max(3.0)
measure_list.append(finn)

fine = bsh_api.measures.ShadeFin(orientation='e')
fine.set_min(0)
fine.set_max(3.0)
measure_list.append(fine)

finw = bsh_api.measures.ShadeFin(orientation='w')
finw.set_min(0)
finw.set_max(3.0)
measure_list.append(finw)

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
measure_list.append(lpd)

winu = bsh_api.measures.WindowUValue(orientation='s')
winu.set_min(1.2)
winu.set_max(3.7)
measure_list.append(winu)

winshgc = bsh_api.measures.WindowSHGC('s')
winshgc.set_min(0.2)
winshgc.set_max(0.8)
measure_list.append(winshgc)

winun = bsh_api.measures.WindowUValue(orientation='n')
winun.set_min(1.2)
winun.set_max(3.7)
measure_list.append(winun)

winshgcn = bsh_api.measures.WindowSHGC('n')
winshgcn.set_min(0.2)
winshgcn.set_max(0.8)
measure_list.append(winshgcn)

winue = bsh_api.measures.WindowUValue(orientation='e')
winue.set_min(1.2)
winue.set_max(3.7)
measure_list.append(winue)

winshgce = bsh_api.measures.WindowSHGC('e')
winshgce.set_min(0.2)
winshgce.set_max(0.8)
measure_list.append(winshgce)

winuw = bsh_api.measures.WindowUValue(orientation='w')
winuw.set_min(1.2)
winuw.set_max(3.7)
measure_list.append(winuw)

winshgcw = bsh_api.measures.WindowSHGC('w')
winshgcw.set_min(0.2)
winshgcw.set_max(0.8)
measure_list.append(winshgcw)

chillerEff = bsh_api.measures.CoolingChillerCOP()
chillerEff.set_min(3.5)
chillerEff.set_max(5.5)
measure_list.append(chillerEff)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

# Add EEMs to parametric job
new_pj.add_model_measures(measure_list)

# Start!
if model_api_key is not None and model_api_key != '':
    results = new_pj.submit_parametric_study(model_api_key=model_api_key, unit='si', algorithm='montecarlo',
                                             size=number_of_simulation, track=True)
elif local_file_dir is not None and local_file_dir != '':
    results = new_pj.submit_parametric_study_local(local_file_dir, unit='si', epw_dir=wea_dir, algorithm='montecarlo', size=number_of_simulation,
                                                   track=True)
