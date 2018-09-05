import BuildSimHubAPI as bsh_api

# 1. set your folder key
project_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_key = 'e17244c9-922a-4ac7-9506-a1d0880755f6'
local_file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"

bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

measure_list = list()

wwrn = bsh_api.measures.WindowWallRatio(orientation="N")
wwrn.set_data(0.3)
measure_list.append(wwrn)

wwrs = bsh_api.measures.WindowWallRatio(orientation="S")
wwrs.set_data(0.3)
measure_list.append(wwrs)

wwrw = bsh_api.measures.WindowWallRatio(orientation="W")
wwrw.set_data(0.3)
measure_list.append(wwrw)

wwre = bsh_api.measures.WindowWallRatio(orientation="E")
wwre.set_data(0.3)
measure_list.append(wwre)

wallr = bsh_api.measures.WallRValue('ip')
wallr.set_data(40)
measure_list.append(wallr)

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_data(0.6)
measure_list.append(lpd)

chillerEff = bsh_api.measures.CoolingChillerCOP()
chillerEff.set_data(5.5)
measure_list.append(chillerEff)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_data(0.95)
measure_list.append(heatEff)

model = bsh.model_results(project_key, model_key)
new_key = model.model_copy(project_key)
new_model = bsh.model_results(project_key, new_key)
updated_measure_key = new_model.apply_measures(measure_list)


new_sj = bsh.new_simulation_job(project_key)
result = new_sj.run_model_simulation(track_token=updated_measure_key, track=True)
print(result.net_site_eui())

