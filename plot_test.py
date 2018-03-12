import BuildSimHubAPI as bsh_api

usr_key = '94266512-c5ea-463d-a108-9dd1e84c07ca'
model_key = '5dc2b500-7821-4c2a-b27c-266fdbdddb40'

results = bsh_api.helpers.ParametricModel(usr_key, model_key)

result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit
print(result_dict)

plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)
plot.scatter_chart_plotly()
#plot.parallel_coordinate_plotly('LPD')
