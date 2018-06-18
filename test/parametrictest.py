"""
Sample code to demonstrate a parametric workflow

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# 1. set your folder key
project_key = 'f698ff06-4388-4549-8a29-e227dbc7b696'
# model_key = '48003d7a-143f-45c1-b175-4ab4d1968bbd'

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"

bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_key)

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
results = new_pj.submit_parametric_study_local(file_dir, track=True)

if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    print(plot.pandas_df())

    plot.scatter_chart_plotly("Scatter plot demo")
    plot.parallel_coordinate_plotly('LPD')