import BuildSimHubAPI as bsh_api

usr_key = '94266512-c5ea-463d-a108-9dd1e84c07ca'
model_key = '77510e51-f169-4474-ab35-bc207f05e0ff'

results = bsh_api.helpers.ParametricModel(usr_key, model_key)

result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit
print(result_dict)

plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)
plot.parallel_coordinate_plotly()
