"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT?
This script demonstrates how to retrieve load components data of a zone in the building after a successful simulation
and how to plot a sankey chart to demonstrate the load distributions

HOW TO USE THE SCRIPT?
Replace the project_api_key and model_api_key with your model
Replace the report name - typically in the content of the HTML
Replace the zone name - the name of the zone - load components

PACKAGE REQUIRED:
Plotly

"""

import BuildSimHubAPI as bshapi
import os
from plotly.offline import plot

"""
INPUT
"""
# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = 'aa09eabf-693f-4437-88cc-a522a25fba01'
zone_name = 'SPACE1-1'

"""
SCRIPT
"""
color_map = ["rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)",
             "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)",
             "rgba(188, 189, 34, 0.8)",  "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)",
             "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)",
             "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)",
             "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)",
             "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)",
             "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)",
             "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "magenta",
             "rgba(227, 119, 194, 0.8)",  "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)",
             "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)",
             "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)",
             "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)",
             "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "magenta"]

# initialize the client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
results = bsh.model_results(project_api_key, model_api_key)
zone_list = results.zone_list()
for i in range(len(zone_list)):
    zone = zone_list[i]
    print("Zone name: " + zone['zone_name'] + " on Floor: " + str(zone['floor']) + " and is conditioned: "
          + zone['conditioned'])

# put zone name here
one_zone_load_data = results.zone_load(zone_name)[0]
floor_area = one_zone_load_data['floor_area']
floor_area_unit = one_zone_load_data['floor_area_unit']
data = one_zone_load_data['data']

cooling_unit = data['cooling_unit']
heating_unit = data['heating_unit']

# initial values
cooling = data['cooling']
heating = data['heating']
# record the number of component
counter = 0
id_map = dict()
label = []
color_temp = []

for i in range(len(cooling)):
    cooling_comp = cooling[i]
    comp_name = cooling_comp['load_component']
    # we do not want to include the grant total in the sankey chart
    if comp_name != 'Grand Total':
        id_map['Cool: ' + comp_name] = counter
        label.append('Cool: ' + comp_name)
        color_temp.append(color_map[counter])
        counter += 1

id_map['Sensible - Instant'] = counter
label.append('Sensible - Instant')
color_temp.append(color_map[counter])
counter += 1

id_map['Sensible - Delayed'] = counter
label.append('Sensible - Delayed')
color_temp.append(color_map[counter])
counter += 1

id_map['Sensible - Return Air'] = counter
label.append('Sensible - Return Air')
color_temp.append(color_map[counter])
counter += 1

id_map['Latent'] = counter
label.append('Latent')
color_temp.append(color_map[counter])
counter += 1

for i in range(len(heating)):
    heating_comp = heating[i]
    comp_name = heating_comp['load_component']
    # we do not want to include the grant total in the sankey chart
    if comp_name != 'Grand Total':
        id_map['Heat: ' + comp_name] = counter
        label.append('Heat: ' + comp_name)
        color_temp.append(color_map[counter])
        counter += 1

target = []
source = []
value = []

for j in range(len(cooling)):
    cooling_comp = cooling[j]
    comp_name = cooling_comp['load_component']
    # we do not want to include the grant total in the sankey chart
    if comp_name != 'Grand Total':
        for key in cooling_comp:
            if key in id_map:
                source.append(id_map['Cool: ' + comp_name])
                target.append(id_map[key])
                value.append(float(cooling_comp[key]))

for k in range(len(heating)):
    heating_comp = heating[k]
    comp_name = heating_comp['load_component']
    # we do not want to include the grant total in the sankey chart
    if comp_name != 'Grand Total':
        for key in heating_comp:
            if key in id_map:
                target.append(id_map['Heat: ' + comp_name])
                source.append(id_map[key])
                value.append(float(heating_comp[key]))


"""
PLOT!
"""
data_trace = dict(
    type='sankey',
    domain=dict(
        x=[0, 1],
        y=[0, 1]
    ),
    orientation='h',
    valueformat='.0f',
    valuesuffix='W',
    node=dict(
        pad=15,
        thickness=15,
        line=dict(
            color='black',
            width=0.5
        ),
        label=label,
        color=color_temp
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
    )
)

layout = dict(
    title=zone_name + ' load components',
    font=dict(
        size=10
    )
)
dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(dir)
fig = dict(data=[data_trace], layout=layout)
plot(fig, filename=dir + '/load.html')
