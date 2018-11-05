"""
This example shows how to directly retrieve the parametric
results and use plotly integration to do scatter plot and
paralle_coordinate chart plot

"""

import BuildSimHubAPI as bsh_api


# project_key can be found in every project (click the information icon next to project name)
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# model_key can be found in each model information bar
model_api_key = '60952acf-bde2-44fa-9883-a0a78bf9eb56'

bsh = bsh_api.BuildSimHubAPIClient()
model = bsh.model_results(project_api_key, model_api_key)
# this will open your default browser to view the 3d geometry
model.bldg_threed()
