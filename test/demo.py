import BuildSimHubAPI as bshapi

file_dir = '/Users/weilixu/Desktop/Presentations/Demo/5ZoneAirCooled_UniformLoading.epJSON'
wea_dir = '/Users/weilixu/Desktop/Presentations/Demo/sanfran.epw'

project_api = 'f698ff06-4388-4549-8a29-e227dbc7b696'

bsh = bshapi.BuildSimHubAPIClient()

new_pj = bsh.new_parametric_job(project_api)

bldg_orientation = bshapi.measures.BuildingOrientation()
bldg_val = [0,90,180,270]
bldg_orientation.set_datalist(bldg_val)
new_pj.add_model_measure(bldg_orientation)




