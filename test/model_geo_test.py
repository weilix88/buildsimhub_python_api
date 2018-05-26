"""
This example shows how to directly retrieve the parametric
results and use plotly integration to do scatter plot and
paralle_coordinate chart plot

"""

import BuildSimHubAPI as bsh_api


project_api_key = ''
model_api_key = ''

model = bsh_api.helpers.Model(project_api_key, model_api_key)
# this will open your default browser to view the 3d geometry
model.bldg_geo()
