"""
This example shows how to directly retrieve the parametric
results and use plotly integration to do scatter plot and
paralle_coordinate chart plot

"""

import BuildSimHubAPI as bsh_api


# project_key can be found in every project (click the information icon next to project name)
project_api_key = "f613129e-69c4-46fc-b1c3-ff7569d50194"
# model_key can be found in each model information bar
model_api_key = "e5326462-447e-4cb6-bb77-cb886b80408b"

model = bsh_api.helpers.Model(project_api_key, model_api_key)
# this will open your default browser to view the 3d geometry
model.bldg_geo()
