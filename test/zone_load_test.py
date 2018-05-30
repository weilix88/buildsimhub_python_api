"""
zone load test
"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "f613129e-69c4-46fc-b1c3-ff7569d50194"
# model_key can be found in each model information bar
model_key = "e5326462-447e-4cb6-bb77-cb886b80408b"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bshapi.helpers.Model(project_key, model_key)

zone_load_data = results.zone_load()
zone_level_load = pp.ZoneLoad(zone_load_data)

print(zone_level_load.get_df())
zone_level_load.load_bar_chart('density')

one_zone_load_data = results.zone_load('CORE_TOP')
one_zone_load = pp.OneZoneLoad(one_zone_load_data)
print(one_zone_load.heating_load_component_detail())
