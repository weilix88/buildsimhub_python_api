import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

project_api_key = ""
model_api_key = ""
results = bsh_api.helpers.ParametricModel(project_api_key, model_api_key)
if results:
    # Collect results
    print("Hello")
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit
    print(result_dict)
    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    print(plot.pandas_df())
    plot.scatter_chart_plotly("Scatter plot demo")
    plot.parallel_coordinate_plotly('LPD')
