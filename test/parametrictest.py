"""
Sample code to demonstrate a parametric workflow

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# 1. set your folder key
project_key = '87e86a33-964e-4809-9e72-802791a8e968'
model_key = '82f244cf-adb6-4f69-9d5d-183ca5e89106'

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"

bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_key, model_key)

# Define EEMs
wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.6, 0.4, 0.3]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2, 0.9, 0.7]
lpd.set_datalist(lpdValue)

heatEff = bsh_api.measures.HeatingEfficiency()
cop = [0.8, 0.86]
heatEff.set_datalist(cop)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(heatEff)

# Start!
results = new_pj.submit_parametric_study_local(file_dir, track=True)

if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)

    plot.scatter_chart_plotly("Scatter plot demo")
    plot.parallel_coordinate_plotly('LPD')