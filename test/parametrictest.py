"""
Sample code to demonstrate a parametric workflow

"""

import BuildSimHubAPI as bsh_api

# 1. set your folder key
model_key = '39ed84d0-062b-470d-96e6-b03abff9c31c'

bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(model_key)

# Define EEMs
wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.6, 0.4, 0.2]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2, 0.9, 0.6]
lpd.set_datalist(lpdValue)

heatEff = bsh_api.measures.HeatingEfficiency()
cop = [0.8, 0.86, 0.92]
heatEff.set_datalist(cop)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(heatEff)

# Start!
results = new_pj.submit_parametric_study(track=True)

if results:

    # Collect results
    results = bsh.get_parametric_results(new_pj)

    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)

    plot.scatter_chart_plotly("Scatter plot demo")
    plot.parallel_coordinate_plotly('LPD')