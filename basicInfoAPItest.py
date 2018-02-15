from BuildSimHubAPI import buildsimhub
import time

bsh = buildsimhub.BuildSimHubAPIClient()

#1. set your folder key
folder_key="0f8ca79b-3952-41c7-89e6-7fbff764a56e"
#2. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
#3. this is optional
comment = "new upload 2"
#4. simulation Type. this is optional
st = bsh.get_simulation_type()
stType = st.regular

newSj = bsh.new_simulation_job(folder_key)
#5. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers
response = newSj.create_model(file_dir, comment)
if(response == 'success'):
  m = newSj.model
  print (m.num_total_floor())
  print (m.num_zones())
  print (m.num_condition_zones())
  print (m.condition_floor_area(""))
  print (m.gross_floor_area("ip"))
  print (m.window_wall_ratio())

  newSj.run_simulation()
  while newSj.track_simulation():
    print (newSj.trackStatus)
    time.sleep(5)
  
  print(m.net_site_eui())
  print(m.total_site_eui())
  print(m.not_met_hour_cooling())
  print(m.not_met_hour_heating())
  print(m.not_met_hour_total())
  print(m.total_end_use_electricity())
  print(m.total_end_use_naturalgas())

else:
  print(response)
