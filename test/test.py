"""

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp
import pandas as pd


file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/data/UnitTest/in.epw"
wea_dir_sf = "/Users/weilixu/Desktop/data/UnitTest/insf.epw"
temp_dir = "/Users/weilixu/Desktop/data/"

# model_key can be found in each model information bar
# paste your project api key
project_api_key = '6e764740-cb49-40ed-8a1a-1331b1d87ed2'
# paste your model api key
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = "e6964bb0-a5a3-437e-b2c1-686f430686b8"

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

parametric = bsh.new_parametric_job(project_api_key)

measurelist = list()

wwr = bshapi.measures.WindowWallRatio(orientation='S')
wwrlist = [0.5]
wwr.set_datalist(wwrlist)
measurelist.append(wwr)

wu = bshapi.measures.WindowUValue(orientation='S')
wulist = [1.4]
wu.set_datalist(wulist)
measurelist.append(wu)

wshgc = bshapi.measures.WindowSHGC(orientation='S')
wshgclist = [0.2]
wshgc.set_datalist(wshgclist)
measurelist.append(wshgc)

parametric.add_model_measures(measurelist)

results = parametric.submit_parametric_study_local(file_dir, track=True)

print(results.net_site_eui())




