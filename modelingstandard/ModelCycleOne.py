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

How to use this python script:
1. Get a BuildSimHub account - it is free of charge and you can get 2 free simulation hours
    by following the walk-through. https://my.buildsim.io/register.html
2. Download the API package from GITHUB
3. Copy the project_api_key from your demo project /  any new projects and paste it to the project_api_key
4. Copy a whole building model from the model library (List of PNNL reference and IECC models)
5. Copy the model_api_key and paste to the variable: model_api_key
6. Define parameters in the lists under model_api_key
7. Run the script!
You are done

Author: Weili Xu
Date: 4/25/2018

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# paste your BuildSimHub project api key here:
project_api_key = '7e140eec-b37f-4213-8640-88b5f96c0065'
# paste your BuildSimHub model api key here:
model_api_key = 'a69753b9-c8f5-40e3-9aa5-e8ac283b1cb4'
# fill in your investigation values
bldg_orientation = []
wwr_south = [0.5, 0.6]
wwr_north = []
wwr_east = []
wwr_west = [0.3, 0.4]
overhang_south = []
overhang_north = []
overhang_east = []
overhang_west = []
fin_south = []
fin_north = []
fin_west = []
fin_east = []
wall_rvalue = []
wall_unit = "ip"
roof_rvalue = []
roof_unit = "ip"
window_uvalue = []
window_u_unit = 'si'
window_shgc = []

"""
Below are the standard API code - You don't need to touch the code below
unless you want to process different types of results than this script.

"""
# Create a new parametric job
bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_api_key, model_api_key)

measures = list()

# Define EEMs
orientation = bsh_api.measures.BuildingOrientation()
orientation.set_datalist(bldg_orientation)
measures.append(orientation)

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

overhangn = bsh_api.measures.ShadeOverhangNorth()
overhangn.set_datalist(overhang_north)
measures.append(overhangn)

overhangs = bsh_api.measures.ShadeOverhangSouth()
overhangs.set_datalist(overhang_south)
measures.append(overhangs)

overhangw = bsh_api.measures.ShadeOverhangWest()
overhangw.set_datalist(overhang_west)
measures.append(overhangw)

overhange = bsh_api.measures.ShadeOverhangEast()
overhange.set_datalist(overhang_east)
measures.append(overhange)

finn = bsh_api.measures.ShadeFinNorth()
finn.set_datalist(fin_north)
measures.append(finn)

fins = bsh_api.measures.ShadeFinSouth()
fins.set_datalist(fin_south)
measures.append(fins)

finw = bsh_api.measures.ShadeFinWest()
finw.set_datalist(fin_west)
measures.append(finw)

fine = bsh_api.measures.ShadeFinEast()
fine.set_datalist(fin_east)
measures.append(fine)

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
print(results)

'''
Below are post-processing code
Results carries the API calls to retrieve your parametric simulations

In this case, we showed two post-process methods:
1. get the results in pandas dataframe
2. plot it in a parallel coordinate chart.
'''
if results:
    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit
    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    print(plot.pandas_df())
    plot.parallel_coordinate_plotly()
