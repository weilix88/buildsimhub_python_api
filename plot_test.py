import BuildSimHubAPI as bsh_api

usr_key = '94266512-c5ea-463d-a108-9dd1e84c07ca'
model_key = '28c2ec3f-fe72-4c8f-a6c1-579fe14297c9'

results = bsh_api.helpers.ParametricModel(usr_key, model_key)
#results = bsh_api.helpers.Model(usr_key, model_key)

#zone_load = results.zone_load('ZN_1_FLR_1_SEC_2')
#print(zone_load)
result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit
print(result_dict)

plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)
plot.parallel_coordinate_plotly()
