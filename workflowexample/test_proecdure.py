
import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "f98aadb3-254f-428d-a321-82a6e4b9424c"

file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/data/UnitTest/in.epw"
# initialize the client
bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

"""
The most straightforward way to do simulation
"""
new_sj_run = bsh.new_simulation_job(project_key)
# results = new_sj_run.run(file_dir, wea_dir, track=True)
results = bsh.model_results(project_key, '2-330-698')

if results:
    assert(results.net_site_eui() == 21.43)
    assert(results.bldg_orientation() == 30.0)
    assert(results.num_above_ground_floor() == 2)
    assert(results.num_total_floor() == 2)
    assert(results.num_zones() == 6.0)
    assert(results.num_condition_zones() == 5.0)
    assert(results.condition_floor_area('si') == 182.48999999999998)
    assert(results.gross_floor_area('si') == 927.1999999999999)
    assert(results.window_wall_ratio() == 0.18687089715536104)
    assert(results.total_site_eui() == 21.43)
    assert(results.not_met_hour_cooling() == 57.75)
    assert(results.not_met_hour_heating() == 3.25)
    assert(results.total_end_use_electricity() == 148881.28)
    assert(results.total_end_use_naturalgas() == 64993.26)
    assert(results.cooling_electricity() == 15751.18)
    assert(results.cooling_naturalgas() == 0.0)
    assert(results.domestic_hotwater_electricity() == 0.0)
    assert(results.domestic_hotwater_naturalgas() == 0.0)
    assert(results.exterior_equipment_electricity() == 0.0)
    assert(results.exterior_equipment_naturalgas() == 0.0)
    assert(results.exterior_lighting_electricity() == 0.0)
    assert(results.exterior_lighting_naturalgas() == 0.0)
    assert(results.fan_electricity() == 8417.7)
    assert(results.fan_naturalgas() == 0.0)
    assert(results.heating_electricity() == 0.0)
    assert(results.heating_naturalgas() == 64993.26)
    assert(results.heat_rejection_electricity() == 0.0)
    assert(results.heat_rejection_naturalgas() == 0.0)
    assert(results.interior_equipment_electricity() == 45238.33)
    assert(results.interior_equipment_naturalgas() == 0.0)
    assert(results.interior_lighting_electricity() == 77051.08)
    assert(results.interior_lighting_naturalgas() == 0.0)
    assert(results.pumps_electricity() == 2422.98)
    assert(results.pumps_naturalgas() == 0.0)
    assert(results.bldg_lpd() == 5.127605283300905)
    assert(results.bldg_epd() == 1.7092069856841865)
    assert(results.wall_rvalue() == 13.88888888888889)
    assert(results.roof_rvalue() == 20)
    assert(results.window_uvalue() == 0.7585)
    assert(results.window_shgc() == 0.49333333333333335)
    assert(results.roof_absorption() == 0.35)
    assert(results.bldg_infiltration() == 0.05757919971127442)
    assert(results.bldg_dx_cooling_efficiency() == -1)
    assert(results.bldg_chiller_efficiency() == 3.2)
    assert(results.bldg_electric_boiler_efficiency() == -1)
    assert(results.bldg_fuel_boiler_efficiency() == 0.8)
    assert(results.bldg_dx_heating_efficiency() == -1)
