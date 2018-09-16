"""
This example shows how to get a value from a model by using class label and field name

the field name can also be replaced by filed index
and user can also specify the class name to extract a the value for a particular class.

"""

import BuildSimHubAPI as bshapi
import pandas as pd

project_api_key = '8b7a41d1-f05a-49cd-8a58-d9ec41b00ab0'
model_api_key = '9d21ac7d-50ea-48ca-b9c0-3cee601d0834'

bsh = bshapi.BuildSimHubAPIClient()

model = bsh.model_results(project_api_key, model_api_key)

# data = model.get_value("Lights", field_index = 5)
# data = model.get_value("Lights", "Watts per Zone Floor Area", class_name="Basement_Lights")
data = model.get_value("Lights", "Watts per Zone Floor Area")
df = pd.DataFrame(data)
print(df.to_string())
'''
print:
                          key                       name  value
0   Watts per Zone Floor Area            Basement_Lights  10.76
1   Watts per Zone Floor Area         Core_bottom_Lights  10.76
2   Watts per Zone Floor Area            Core_mid_Lights  10.76
3   Watts per Zone Floor Area            Core_top_Lights  10.76
4   Watts per Zone Floor Area  Perimeter_bot_ZN_1_Lights  10.76
5   Watts per Zone Floor Area  Perimeter_bot_ZN_2_Lights  10.76
6   Watts per Zone Floor Area  Perimeter_bot_ZN_3_Lights  10.76
7   Watts per Zone Floor Area  Perimeter_bot_ZN_4_Lights  10.76
8   Watts per Zone Floor Area  Perimeter_mid_ZN_1_Lights  10.76
9   Watts per Zone Floor Area  Perimeter_mid_ZN_2_Lights  10.76
10  Watts per Zone Floor Area  Perimeter_mid_ZN_3_Lights  10.76
11  Watts per Zone Floor Area  Perimeter_mid_ZN_4_Lights  10.76
12  Watts per Zone Floor Area  Perimeter_top_ZN_1_Lights  10.76
13  Watts per Zone Floor Area  Perimeter_top_ZN_2_Lights  10.76
14  Watts per Zone Floor Area  Perimeter_top_ZN_3_Lights  10.76
15  Watts per Zone Floor Area  Perimeter_top_ZN_4_Lights  10.76

'''