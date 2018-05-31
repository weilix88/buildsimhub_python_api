"""
This file contains a workflow for modeling cycle # 3 in ASHRAE Standard 209:
Energy Simulation Aided Design for Buildings except Low-Rise Residential Buildings (ANSI Approved)

Modeling cycle 3 analysis:
Develop a list of at least three peak load reduction strategies selected from one or more of the following categories:
a. Building envelope (including, but not limited to, insulation level, window-to-wall ratio, glazing performance,
shading, infiltration, phase change materials, and thermal mass)
b. Lighting and daylighting
c. Internal equipment loads
d. Outdoor air (including, but not limited to, outdoor airflow,exhaust air, and energy recovery)
e. Passive conditioning and natural ventilation
When internal equipment loads exceed 60% of the building energy end use, at least two of the strategies shall be
selected from the internal equipment loads category.

This script covers most of the measures including:
a: insulation level, wwr, window u and SHGC and infiltration
b: lighting, daylighting and occupancy control
c. Internal equipment loads

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
project_api_key = "b2809d88-847d-474e-91a5-8763b6b81a27"
# paste your BuildSimHub model api key here:
model_api_key = "babac3ee-9fd0-4d62-8f5d-6fd706492607"
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
wall_rvalue = [20, 30]
wall_unit = "ip"
roof_rvalue = []
roof_unit = "ip"
window_uvalue = []
window_u_unit = 'ip'
window_shgc = []

"""
Below are the standard API code - You don't need to touch the code below
unless you want to process different types of results than this script.

"""