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
project_key = '00787f31-1655-4653-b624-82656e9fed95'
model_api_key = None
local_file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
number_of_simulation = 10

bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
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

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
light_temp = bsh_api.helpers.DesignTemplate()
light_temp.set_class_label("Lights")
light_temp.set_template_field("Return Air Fraction", "0.2")
light_temp.set_template_field("Fraction Radiant", "0.6")
lpd.set_custom_template(light_temp)
measure_list.append(lpd)

chillerEff = bsh_api.measures.CoolingChillerCOP()
chillerEff.set_min(3.5)
chillerEff.set_max(5.5)
measure_list.append(chillerEff)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

hvac = bsh_api.measures.HVACTemplate()
hvac.set_min(0)
hvac.set_max(2)
measure_list.append(hvac)

# Add EEMs to parametric job
new_pj.add_model_measures(measure_list)

# Start!
if model_api_key is not None and model_api_key != '':
    results = new_pj.submit_parametric_study(model_api_key=model_api_key, algorithm='montecarlo',
                                             size=number_of_simulation, track=True)
elif local_file_dir is not None and local_file_dir != '':
    results = new_pj.submit_parametric_study_local(local_file_dir, algorithm='montecarlo', size=number_of_simulation,
                                                   track=True)
