import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()

# 1. set your folder key
model_key="08c56285-93c4-4656-9dce-d7efebc7fc8d"
# 2. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
# 3. this is optional
comment = "new upload 2"
# 4. simulation Type. this is optional
st = bsh.get_simulation_type()
st.set_regular()

newSj = bsh.new_simulation_job(model_key)

# 5. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers
response = newSj.create_model(file_dir, comment)
if response == 'success':
    m = bsh.get_model(newSj)
    print(str(m.num_total_floor()) + " " + m.last_parameter_unit)
    print(str(m.num_zones()) + " " + m.last_parameter_unit)
    print(str(m.num_condition_zones()) + " " + m.last_parameter_unit)
    print(str(m.condition_floor_area("")) + " " + m.last_parameter_unit)
    print(str(m.gross_floor_area("ip")) + " " + m.last_parameter_unit)
    print(str(m.window_wall_ratio()) + " " + m.last_parameter_unit)

    newSj.run_model_simulation(st.type, st.agent, track=True)

    print(str(m.net_site_eui()) + " " + m.last_parameter_unit)
    print(str(m.total_site_eui()) + " " + m.last_parameter_unit)
    print(str(m.not_met_hour_cooling()) + " " + m.last_parameter_unit)
    print(str(m.not_met_hour_heating()) + " " + m.last_parameter_unit)
    # print(str(m.not_met_hour_total()) + " " + m.lastParameterUnit)
    print(str(m.total_end_use_electricity()) + " " + m.last_parameter_unit)
    print(str(m.total_end_use_naturalgas()) + " " + m.last_parameter_unit)

    load_profile = m.zone_load()
    print(load_profile)
    zl = bshapi.postprocess.ZoneLoad(load_profile)
    print(zl.get_df())

else:
    print(response)
