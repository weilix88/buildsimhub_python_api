"""
Sample code to demonstrate a parametric workflow

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# 1. set your folder key
project_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key = '48003d7a-143f-45c1-b175-4ab4d1968bbd'

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"

bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
new_pj = bsh.new_parametric_job(project_key)

# Define EEMs
measure_list = list()

wwr = bsh_api.measures.WindowWallRatio()
wwr.set_min(0.3)
wwr.set_max(0.6)
measure_list.append(wwr)

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
measure_list.append(lpd)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

# Add EEMs to parametric job
new_pj.add_model_measures(measure_list)

# Start!
results = new_pj.submit_parametric_study_local(file_dir, algorithm='montecarlo', size=10, track=True)
print(results)
# if the seed model is on the Buildsim cloud - use this method:
# results = new_pj.submit_parametric_study(track=True)

if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    print(plot.pandas_df())

    plot.scatter_chart_plot("Scatter plot demo")
    plot.parallel_coordinate_plot('LPD')
