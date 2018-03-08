import BuildSimHubAPI as bsh_api

usr_key = '94266512-c5ea-463d-a108-9dd1e84c07ca'
# model_key = '4ea80e1c-3150-479c-9eca-0da0531720f6'

# results = bsh_api.helpers.ParametricModel(usr_key, model_key)

# result_dict = results.net_site_eui()
# result_unit = results.lastParameterUnit
# print(result_dict)

model_key = "fe9d9b81-4348-4162-a170-39e86abdd949"
buildsimhub = bsh_api.BuildSimHubAPIClient()
model = bsh_api.helpers.Model(buildsimhub.userAPI, model_key)
print(model.num_zones())



