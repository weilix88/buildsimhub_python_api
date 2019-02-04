
import BuildSimHubAPI as bshapi
import pandas as pd

# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'c39dceed-242b-4ea3-9fd4-e2076f89c29b'
# model_key can be found in each model information bar
model_api_key = 'dca5f246-e6b5-44de-8a31-b9e27e28a633'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_api_key, model_api_key)
zone_list = results.zone_list()

zone_group = dict()
for zone in zone_list:
    zone_group[zone['zone_name']] = dict()
    zone_group[zone['zone_name']]['ventilation'] = 'testzone'
    floor = zone['floor']
    if floor == 2:
        zone_group[zone['zone_name']]['heating'] = 'test2zone'
        zone_group[zone['zone_name']]['cooling'] = 'test2zone'
    else:
        zone_group[zone['zone_name']]['heating'] = 'test3zone'
        zone_group[zone['zone_name']]['cooling'] = 'test3zone'

print(zone_group)

id = results.hvac_swap('/Users/weilixu/Desktop/doasfancoil.idf', zone_group=zone_group)

sim_update = bsh.new_simulation_job(project_api_key)
update_model = sim_update.run_model_simulation(id, track=True)
print(update_model.net_site_eui())



