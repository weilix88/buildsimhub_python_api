import BuildSimHubAPI as bsh_api

usr_key = '94266512-c5ea-463d-a108-9dd1e84c07ca'
# model_key = '4ea80e1c-3150-479c-9eca-0da0531720f6'

# results = bsh_api.helpers.ParametricModel(usr_key, model_key)

# result_dict = results.net_site_eui()
# result_unit = results.lastParameterUnit
# print(result_dict)


model_key = "693fb698-ece5-418c-9810-de90bddc6d35"
results = bsh_api.helpers.Model(usr_key, model_key)
load_profile = results.zone_load()
print(load_profile)
zl = bsh_api.postprocess.ZoneLoad(load_profile)
print(zl.get_df())


