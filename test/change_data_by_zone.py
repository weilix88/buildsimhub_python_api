"""
This example demonstrates how to change data by zones

The user needs to define the object template in a list of dictionary -
each dictionary contains the data that the user wants to change.

It also needs a list of zones that the user wants to apply the measure to.
"""

import BuildSimHubAPI as bshapi

project_api_key = '8b7a41d1-f05a-49cd-8a58-d9ec41b00ab0'
model_api_key = '9d21ac7d-50ea-48ca-b9c0-3cee601d0834'

bsh = bshapi.BuildSimHubAPIClient()
model = bsh.model_results(project_api_key, model_api_key)

# initialize the parameters
data = list()
light = bshapi.helpers.EnergyPlusObject('Lights')
equip = bshapi.helpers.EnergyPlusObject('ElectricEquipment')

# set-up template for lights and electric equipment
light.add_field_template('Design Level Calculation Method', "LightingLevel")
light.add_field_template('Lighting Level', "100")

equip.add_field_template('Design Level Calculation Method', "EquipmentLevel")
equip.add_field_template('Design Level', "120")

data.append(light)
data.append(equip)

# initialize the zone list
zone_list = list()
zone_list.append("Perimeter_top_ZN_3")
zone_list.append("Perimeter_top_ZN_4")

# modify the zone and get the new ID
tracking = model.add_modify_zone(zone_list, data)
print(tracking)
