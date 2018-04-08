import BuildSimHubAPI as bsh_api
import time

# 1. set your folder key
model_key = '553de3da-a092-4245-a456-3f81f036a6db'

bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(model_key)

# Define EEMs
dds = bsh_api.measures.DaylightingSensor()

# Add EEMs to parametric job
new_pj.add_model_measure(dds)

# Start!
results = new_pj.submit_parametric_study(track=True, unit='si')

if results:

    # Collect results
    results = bsh.get_parametric_results(new_pj)

    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)

    plot.scatter_chart_plotly("Scatter plot demo")
    plot.parallel_coordinate_plotly('LPD')
