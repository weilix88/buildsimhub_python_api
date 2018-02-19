from src/BuildSimHubAPI import buildsimhub
import time

bsh = buildsimhub.BuildSimHubAPIClient()

#1. set your folder key
model_key="0dde5a46-4d07-4b99-907f-0cfedf301072"
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
response = newSj.create_model(file_dir, comment, st.type, st.agent)
if(response == 'success'):
  while newSj.track_simulation():
    print (newSj.trackStatus)
    time.sleep(5)

  response = newSj.get_simulation_results('err')
  print(response)
else:
  print(response)
