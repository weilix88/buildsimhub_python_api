import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

project_api_key = "771e8"
model_api_key = "17-862d-d758626bc110"
bsh = bsh_api.BuildSimHubAPIClient(base_url='http://my.buildsim.io:8080/IDFVersionControl/')

results = bsh.parametric_results(project_api_key, model_api_key)
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
