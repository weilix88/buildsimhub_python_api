"""
Sample code to demonstrate a parametric workflow

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# 1. set your folder key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'

file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"

bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
new_pj = bsh.new_parametric_job(project_api_key)

# Define EEMs
wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.6, 0.4]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2, 0.9]
lpd.set_datalist(lpdValue)

heatEff = bsh_api.measures.HeatingEfficiency()
cop = [0.8, 0.86]
heatEff.set_datalist(cop)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(heatEff)

# Start!
results = new_pj.submit_parametric_study_local(file_dir, algorithm='opat', track=True)
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
