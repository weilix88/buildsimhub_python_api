import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

project_api_key = "771ec223-482c-4aef-acab-0504735d9e78"
model_api_key = "17475332-3683-40e1-862d-d758626bc110"
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
