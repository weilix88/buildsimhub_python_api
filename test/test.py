"""

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp
import pandas as pd


file_dir = "/Users/weilixu/Desktop/data/smalloffice.idf"
wea_dir = "/Users/weilixu/Desktop/data/UnitTest/in.epw"
wea_dir_sf = "/Users/weilixu/Desktop/data/UnitTest/insf.epw"
temp_dir = "/Users/weilixu/Desktop/data/"

# model_key can be found in each model information bar
# paste your project api key
project_api_key = '6e764740-cb49-40ed-8a1a-1331b1d87ed2'
# paste your model api key
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = '63db4fe3-929f-44cb-9a83-07dc4855aa10'

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
parametric = bsh.new_parametric_job(project_api_key)

measure_list = list()

win_u_s = bshapi.measures.WindowUValue(orientation='S')
win_u_s.set_datalist([1.4, 1.6, 2.0, 2.5, 2.9, 1.4, 1.6, 2.0, 2.5, 2.9])
measure_list.append(win_u_s)

win_shgc_s = bshapi.measures.WindowSHGC(orientation='S')
win_shgc_s.set_datalist([0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4])
measure_list.append(win_shgc_s)

parametric.add_model_measures(measure_list)
parametric.submit_parametric_study_local(file_dir, track=True, algorithm='opat')




