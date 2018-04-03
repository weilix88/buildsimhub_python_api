import BuildSimHubAPI as bsh_api
import webbrowser

usr_key = ''
model_key = ''

# results = bsh_api.helpers.ParametricModel(usr_key, model_key)

# result_dict = results.net_site_eui()
# result_unit = results.last_parameter_unit
# print(result_dict)

# plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)
# print(plot.pandas_df())
# plot.scatter_chart_plotly()
# plot.parallel_coordinate_plotly('LPD')

model = bsh_api.helpers.Model(usr_key, model_key, base_url='https://develop.buildsimhub.net/')

model.bldg_geo()
