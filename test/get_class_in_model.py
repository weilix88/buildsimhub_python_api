"""
This example shows how to get class from a model by using class label

user can also specify the class name to extract a the value for a particular class.

"""

import BuildSimHubAPI as bshapi
import pandas as pd

project_api_key = '8b7a41d1-f05a-49cd-8a58-d9ec41b00ab0'
model_api_key = '9d21ac7d-50ea-48ca-b9c0-3cee601d0834'

bsh = bshapi.BuildSimHubAPIClient()

model = bsh.model_results(project_api_key, model_api_key)

data = model.get_class("Lights")
df = pd.DataFrame(data)
print(df.to_string())

'''
   Design Level Calculation Method End-Use Subcategory Fraction Radiant Fraction Replaceable Fraction Visible Lighting Level                       Name Return Air Fraction Return Air Fraction Calculated from Plenum Temperature   Schedule Name Watts per Person Watts per Zone Floor Area Zone or ZoneList Name   label
0                       Watts/Area             General           0.7000               1.0000           0.2000                           Basement_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76              Basement  Lights
1                       Watts/Area             General           0.7000               1.0000           0.2000                        Core_bottom_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76           Core_bottom  Lights
2                       Watts/Area             General           0.7000               1.0000           0.2000                           Core_mid_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76              Core_mid  Lights
3                       Watts/Area             General           0.7000               1.0000           0.2000                           Core_top_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76              Core_top  Lights
4                       Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_bot_ZN_1_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_bot_ZN_1  Lights
5                       Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_bot_ZN_2_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_bot_ZN_2  Lights
6                       Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_bot_ZN_3_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_bot_ZN_3  Lights
7                       Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_bot_ZN_4_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_bot_ZN_4  Lights
8                       Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_mid_ZN_1_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_mid_ZN_1  Lights
9                       Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_mid_ZN_2_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_mid_ZN_2  Lights
10                      Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_mid_ZN_3_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_mid_ZN_3  Lights
11                      Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_mid_ZN_4_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_mid_ZN_4  Lights
12                      Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_top_ZN_1_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_top_ZN_1  Lights
13                      Watts/Area             General           0.7000               1.0000           0.2000                 Perimeter_top_ZN_2_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_top_ZN_2  Lights
14                   LightingLevel             General           0.7000               1.0000           0.2000            100  Perimeter_top_ZN_3_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_top_ZN_3  Lights
15                   LightingLevel             General           0.7000               1.0000           0.2000            100  Perimeter_top_ZN_4_Lights              0.0000                                                 No      BLDG_LIGHT_SCH                                      10.76    Perimeter_top_ZN_4  Lights

'''
