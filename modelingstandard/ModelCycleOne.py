"""
This file contains a workflow for modeling cycle # 1 in ASHRAE Standard 209:
Energy Simulation Aided Design for Buildings except Low-Rise Residential Buildings (ANSI Approved)

Modeling cycle 1 analysis:
Create energy models to calculate annual building energy by end use and peak heating and cooling loads with identical
HVAC systems. Perform a sensitivity analysis by varying the following building characteristics:
a. Building geometry
b. Window-to-wall ratio, by orientation, and shading options
(if applicable)
c. Orientation
d. Thermal performance of the envelope and structure

Author: Weili Xu
Date: 4/25/2018

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# paste your BuildSimHub project api key here:
project_api_key = '565fcbbc-f500-4548-afb2-bxxxxxxxxx'
# paste your BuildSimHub model api key here:
model_api_key = '565fcbbc-f500-4548-afb2-bxxxxxxxxx'
# fill in your investigation values
wwr_south = [0.5, 0.6]
wwr_north = [0.3, 0.4]
wwr_east = [0.3, 0.4]
wwr_west = [0.3, 0.4]
wall_rvalue = [20, 30]
wall_unit = "ip"
roof_rvalue = [30, 40]
roof_unit = "ip"
window_uvalue = [2.8, 1.4]
window_u_unit = "si"
window_shgc = [0.3, 0.5]

"""
Below are the standard API code
"""
# Create a new parametric job
bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_api_key, model_api_key)

measures = list()

# Define EEMs
wwrs = bsh_api.measures.WindowWallRatioSouth()
wwrs.set_datalist(wwr_south)
measures.append(wwrs)

wwrn = bsh_api.measures.WindowWallRatioNorth()
wwrn.set_datalist(wwr_north)
measures.append(wwrn)

wwrw = bsh_api.measures.WindowWallRatioWest()
wwrw.set_datalist(wwr_west)
measures.append(wwrw)

wwre = bsh_api.measures.WindowWallRatioEast()
wwre.set_datalist(wwr_east)
measures.append(wwre)

wallr = bsh_api.measures.WallRValue(wall_unit)
wallr.set_datalist(wall_rvalue)
measures.append(wallr)

roofr = bsh_api.measures.RoofRValue(roof_unit)
roofr.set_datalist(roof_rvalue)
measures.append(roofr)

winu = bsh_api.measures.WindowUValue(window_u_unit)
winu.set_datalist(window_uvalue)
measures.append(winu)

winshgc = bsh_api.measures.WindowSHGC()
winshgc.set_datalist(window_shgc)
measures.append(winshgc)

# Add measures to the new parametric study
new_pj.add_model_measures(measures)

# Now we start!
results = new_pj.submit_parametric_study(track=True)

if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit
    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    print(plot.pandas_df())
    plot.parallel_coordinate_plotly()





