"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT?
This script demonstrates how to retrieve load components data of a zone in the building after a successful simulation
and also how to plot bar chart based on zone component types (sensible, latent...).

HOW TO USE THE SCRIPT?
Replace the project_api_key and model_api_key with your model
Replace the report name - typically in the content of the HTML
Replace the zone name - the name of the zone - load components
Replace the zone component load type: cooling or heating - this specify which type of load to plot

PACKAGE REQUIRED:
Pandas, Plotly

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp

"""
INPUT
"""
# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = 'aa09eabf-693f-4437-88cc-a522a25fba01'
zone_name = 'SPACE1-1'
zone_component_load_type = 'cooling'

"""
SCRIPT
"""
# initialize the client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
results = bsh.model_results(project_api_key, model_api_key)
zone_list = results.zone_list()
for i in range(len(zone_list)):
    zone = zone_list[i]
    print("Zone name: " + zone['zone_name'] + " on Floor: " + str(zone['floor']) + " and is conditioned: "
          + zone['conditioned'])


"""
PLOT!
"""
# put zone name here
one_zone_load_data = results.zone_load(zone_name)
one_zone_load = pp.OneZoneLoad(one_zone_load_data)
# heating or cooling
one_zone_load.load_type_plot(zone_component_load_type)
