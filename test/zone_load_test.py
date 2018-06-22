"""
zone load test

Make sure you have the latest python plotly installed
pip: pip install plotly
or update: pip install plotly --upgrade

If you have python 2 and 3 installed on your computer, try:
pip3 install plotly

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "f613129e-69c4-46fc-b1c3-ff7569d50194"
# model_key can be found in each model information bar
model_key = "e5326462-447e-4cb6-bb77-cb886b80408b"

# initialize the client
bsh = bshapi.BuildSimHubAPIClient()
results = bsh.model_results(project_key, model_key)

zone_load_data = results.zone_load()
zone_level_load = pp.ZoneLoad(zone_load_data)

print(zone_level_load.pandas_df())
zone_level_load.load_bar_chart_plot('density')

one_zone_load_data = results.zone_load('CORE_TOP')
one_zone_load = pp.OneZoneLoad(one_zone_load_data)
print(one_zone_load.heating_load_component_detail())
one_zone_load.load_component_plot('cooling')
