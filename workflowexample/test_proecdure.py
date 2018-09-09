
import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'

file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/data/UnitTest/in.epw"
# initialize the client
bsh = bsh_api.BuildSimHubAPIClient()

"""
The most straightforward way to do simulation
"""
new_sj_run_temp = bsh.new_simulation_job(project_key)
results = new_sj_run_temp.run(file_dir, wea_dir, track=True)
assert(results == False)
# results = bsh.model_results(project_key, '2-330-698')

new_sj_run = bsh.new_simulation_job(project_customized_key)
results = new_sj_run.run(file_dir, wea_dir, track=True)

if results:
    print(results.net_site_eui())
    assert(results.net_site_eui() == 17.88)
    print(results.bldg_orientation())
    assert(results.bldg_orientation() == 30.0)
    print(results.num_above_ground_floor())
    assert(results.num_above_ground_floor() == 2)
    print(results.num_total_floor())
    assert(results.num_total_floor() == 2)
    print(results.num_zones())
    assert(results.num_zones() == 6.0)
    print(results.num_condition_zones())
    assert(results.num_condition_zones() == 5.0)
    print(results.condition_floor_area('si'))
    assert(results.condition_floor_area('si') == 182.48999999999998)
    print(results.gross_floor_area('si'))
    assert(results.gross_floor_area('si') == 927.1999999999999)
    print(results.window_wall_ratio())
    assert(results.window_wall_ratio() == 18.687089715536104)
    print(results.total_site_eui())
    assert(results.total_site_eui() == 21.43)
    print(results.not_met_hour_cooling())
    assert(results.not_met_hour_cooling() == 57.75)
    print(results.not_met_hour_heating())
    assert(results.not_met_hour_heating() == 3.25)
    print(results.total_end_use_electricity())
    assert(results.total_end_use_electricity() == 148881.28)
    print(results.total_end_use_naturalgas())
    assert(results.total_end_use_naturalgas() == 64993.26)
    print(results.cooling_electricity())
    assert(results.cooling_electricity() == 15751.18)
    print(results.cooling_naturalgas())
    assert(results.cooling_naturalgas() == 0.0)
    print(results.domestic_hotwater_electricity())
    assert(results.domestic_hotwater_electricity() == 0.0)
    print(results.domestic_hotwater_naturalgas())
    assert(results.domestic_hotwater_naturalgas() == 0.0)
    print(results.exterior_equipment_electricity())
    assert(results.exterior_equipment_electricity() == 0.0)
    print(results.exterior_equipment_naturalgas())
    assert(results.exterior_equipment_naturalgas() == 0.0)
    print(results.exterior_lighting_electricity())
    assert(results.exterior_lighting_electricity() == 0.0)
    print(results.exterior_lighting_naturalgas())
    assert(results.exterior_lighting_naturalgas() == 0.0)
    print(results.fan_electricity())
    assert(results.fan_electricity() == 8417.7)
    print(results.fan_naturalgas())
    assert(results.fan_naturalgas() == 0.0)
    print(results.heating_electricity())
    assert(results.heating_electricity() == 0.0)
    print(results.heating_naturalgas())
    assert(results.heating_naturalgas() == 64993.26)
    print(results.heat_rejection_electricity())
    assert(results.heat_rejection_electricity() == 0.0)
    print(results.heat_rejection_naturalgas())
    assert(results.heat_rejection_naturalgas() == 0.0)
    print(results.interior_equipment_electricity())
    assert(results.interior_equipment_electricity() == 45238.33)
    print(results.interior_equipment_naturalgas())
    assert(results.interior_equipment_naturalgas() == 0.0)
    print(results.interior_lighting_electricity())
    assert(results.interior_lighting_electricity() == 77051.08)
    print(results.interior_lighting_naturalgas())
    assert(results.interior_lighting_naturalgas() == 0.0)
    print(results.pumps_electricity())
    assert(results.pumps_electricity() == 2422.98)
    print(results.pumps_naturalgas())
    assert(results.pumps_naturalgas() == 0.0)
    print(results.bldg_lpd())
    assert(results.bldg_lpd() == 5.127605283300905)
    print(results.bldg_epd())
    assert(results.bldg_epd() == 1.7092069856841865)
    print(results.wall_rvalue())
    assert(results.wall_rvalue() == 13.88888888888889)
    print(results.roof_rvalue())
    assert(results.roof_rvalue() == 20)
    print(results.window_uvalue())
    assert(results.window_uvalue() == 0.568)
    print(results.window_shgc())
    assert(results.window_shgc() == 0.756)
    print(results.roof_absorption())
    assert(results.roof_absorption() == 0.35)
    print(results.bldg_infiltration())
    assert(results.bldg_infiltration() == 0.05720000000000001)
    print(results.bldg_dx_cooling_efficiency())
    assert(results.bldg_dx_cooling_efficiency() == -1)
    print(results.bldg_chiller_efficiency())
    assert(results.bldg_chiller_efficiency() == 3.2)
    print(results.bldg_electric_boiler_efficiency())
    assert(results.bldg_electric_boiler_efficiency() == -1)
    print(results.bldg_fuel_boiler_efficiency())
    assert(results.bldg_fuel_boiler_efficiency() == 0.8)
    print(results.bldg_dx_heating_efficiency())
    assert(results.bldg_dx_heating_efficiency() == -1)

"""
Upload your model to a project and run simulation
"""
new_sj_project = bsh.new_simulation_job(project_customized_key)
results = new_sj_project.create_run_model(file_dir, wea_dir, track=True)
model_api_key = new_sj_project.model_api_key

if results:
    zone_load_data = results.zone_load()
    zone_level_load = pp.ZoneLoad(zone_load_data)
    df = zone_level_load.pandas_df()
    print(df['cooling_load'].sum())
    assert(df['cooling_load'].sum() == 116277.3)
    print(df['heating_load'].sum())
    assert(df['heating_load'].sum() == -96021.98)
    one_zone_load_data = results.zone_load('SPACE1-1')
    one_zone_load = pp.OneZoneLoad(one_zone_load_data)
    print(one_zone_load.cooling_load_table()['Total'].sum())
    assert(one_zone_load.cooling_load_table()['Total'].sum() == 12729.5)
    print(one_zone_load.heating_load_table()['Total'].sum())
    assert(one_zone_load.heating_load_table()['Total'].sum() == -13313.98)
    print(one_zone_load.floor_area)
    assert(one_zone_load.floor_area == 1067.45)
    print(one_zone_load.zone_name)
    assert(one_zone_load.zone_name == 'SPACE1-1')
    print(len(results.hourly_data()))
    assert(len(results.hourly_data()) == 87)

new_sj = bsh.new_simulation_job(project_customized_key)
response = new_sj.create_model(file_dir, wea_dir)
results = new_sj.run_model_simulation(track=True)

# new_sj = bsh.new_simulation_job(project_key)
# response = new_sj.create_model(file_dir)
# results = new_sj.run_model_simulation(track=True)

# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
new_pj = bsh.new_parametric_job(project_customized_key, model_api_key)

# Define EEMs
wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.6, 0.4]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2, 0.9]
lpd.set_datalist(lpdValue)

heatEff = bsh_api.measures.HeatingEfficiency()
cop = [0.8, 0.86]
heatEff.set_datalist(cop)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(heatEff)

# Start!
results = new_pj.submit_parametric_study(track=True)
parametric_id = new_pj.track_token

# parametric_id = '6aa21d68-42fd-442e-8bbf-74c32f159a8e'
# results = bsh.parametric_results(project_key, '6aa21d68-42fd-442e-8bbf-74c32f159a8e')
if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    pd = plot.pandas_df()
    print(pd)
    assert(pd['Value'].sum() == 126.77000000000001)

list_data = bsh.model_list(project_customized_key, parametric_id)
model_list = pp.ModelList(bsh.model_list(project_customized_key, parametric_id))
pd = model_list.pandas_df()
print(len(pd))
assert(len(pd) == 8)

########## MONTE CARLO Procedure ######################

new_pj = bsh.new_parametric_job(project_customized_key)

# Define EEMs
measure_list = list()

wwr = bsh_api.measures.WindowWallRatio()
wwr.set_min(0.3)
wwr.set_max(0.6)
measure_list.append(wwr)

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
measure_list.append(lpd)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

# Add EEMs to parametric job
new_pj.add_model_measures(measure_list)

# Start!
results = new_pj.submit_parametric_study_local(file_dir, algorithm='montecarlo', size=10, track=True)
# monte_carlo_id = new_pj.track_token
# results = bsh.parametric_results(project_key, monte_carlo_id)

if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    print(plot.pandas_df()['Value'].sum())
    assert(plot.pandas_df()['Value'].sum() == 130.0)

