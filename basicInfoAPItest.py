from BuildSimHubAPI import buildsimhub
import time

bsh = buildsimhub.BuildSimHubAPIClient()

#1. set your folder key
model_key="0789da9f-6912-4c2b-858d-d6d986234135"
#2. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
#3. this is optional
comment = "new upload 2"
#4. simulation Type. this is optional
st = bsh.get_simulation_type()
st.set_regular()

newSj = bsh.new_simulation_job(model_key)

#5. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers
response = newSj.create_model(file_dir, comment)
if(response == 'success'):
  m = newSj.model
  print (str(m.num_total_floor()) + " " + m.lastParameterUnit)
  print (str(m.num_zones()) + " " + m.lastParameterUnit)
  print (str(m.num_condition_zones()) + " " + m.lastParameterUnit)
  print (str(m.condition_floor_area("")) + " " + m.lastParameterUnit)
  print (str(m.gross_floor_area("ip")) + " " + m.lastParameterUnit)
  print (str(m.window_wall_ratio()) + " " + m.lastParameterUnit)

  newSj.run_simulation()
  while newSj.track_simulation():
    print (newSj.trackStatus)
    time.sleep(5)
  
  print(str(m.net_site_eui())+ " " + m.lastParameterUnit)
  print(str(m.total_site_eui())+ " " + m.lastParameterUnit)
  print(str(m.not_met_hour_cooling())+ " " + m.lastParameterUnit)
  print(str(m.not_met_hour_heating())+ " " + m.lastParameterUnit)
  #print(str(m.not_met_hour_total()) + " " + m.lastParameterUnit)
  print(str(m.total_end_use_electricity())+ " " + m.lastParameterUnit)
  print(str(m.total_end_use_naturalgas())+ " " + m.lastParameterUnit)

else:
  print(response)
