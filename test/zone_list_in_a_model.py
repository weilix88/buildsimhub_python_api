"""
This example demonstrate how to get the zone information of a model.

Currently, all the data in this API call is in SI unit, and non-normalized
e.g. zone_lpd is watt instead of wall/m2
{'zone_name': 'SPACE1-1', 'zone_area': '99.16000000000001', 'zone_ppl': '11.0', 'zone_lpd': '1584.0',
'zone_epd': '1056.0', 'zone_heat': 'VAV Sys 1', 'zone_cool': 'VAV Sys 1', 'zone_vent': 'VAV Sys 1',
'zone_exhaust': ''}

"""
import BuildSimHubAPI as bshapi

# model_key can be found in each model information bar
# paste your model api key
global_project_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = 'f10f9365-ad6f-4f34-b4d8-e598d89af953'

bsh = bshapi.BuildSimHubAPIClient()

model = bsh.model_results(global_project_key, model_api_key)
print(model.zone_info('SPACE1-1'))
