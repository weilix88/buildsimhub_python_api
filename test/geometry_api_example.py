import BuildSimHubAPI as bshapi

project_api_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"
model_api_key = "b86d9ddb-645b-4dad-b96e-1856b5a0ed48"

bsh = bshapi.BuildSimHubAPIClient()
model = bsh.model_results(project_api_key, model_api_key)
display_json = dict()
display_json['type'] = 'zone'  # required: surface or zone
display_json['unit'] = 'Watt'
display_json['color_scale'] = 'yes'  # optional, if color is presented, color scale will be set to no

data = dict()
data['SPACE1-1'] = 26627.78
data['SPACE2-1'] = 11233.23
data['SPACE3-1'] = 25892.06
data['SPACE4-1'] = 11233.23
data['SPACE5-1'] = 21035.68
display_json['data'] = data  # required

# you can pick your own color if the color_scale is set to no
color = dict()
color['SPACE1-1'] = '0x1A535C'  # color format is 0x + RGB hex code
color['SPACE2-1'] = '0x4ECDC4'
color['SPACE3-1'] = '0xF7FFF7'
color['SPACE4-1'] = '0xFF6B6B'
color['SPACE5-1'] = '0xFFE66D'
# display_json['color'] = color

# additional display information
info = dict()
info['SPACE1-1'] = [{'key': 'sensorId', 'value': 'x2232'}]  # color format is 0x + RGB hex code
info['SPACE2-1'] = [{'key': 'sensorId', 'value': 'x2642'}, {'key': 'thermostat', 'value': 32}]
info['SPACE3-1'] = [{'key': 'sensorId', 'value': 'x8392'}]
info['SPACE4-1'] = [{'key': 'sensorId', 'value': 'x3323'}]
info['SPACE5-1'] = [{'key': 'sensorId', 'value': 'x3222'}]
display_json['info'] = info

model.bldg_geo(display_json)



