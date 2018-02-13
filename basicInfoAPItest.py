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
st = bsh.getSimulationType()
stType = st.regular

newSj = bsh.newSimulationJob(folder_key)
#5. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers
response = newSj.createModel(file_dir, comment)
if(response == 'success'):
  m = newSj.model
  print (m.numberOfTotalFloors())
  print (m.numberOfZones())
  print (m.numberOfConditionedZones())
  print (m.conditionedFloorArea("ip"))
  print (m.grossFloorArea("ip"))
  print (m.windowToWallRatio())
  print (m.weatherFileName())
else:
  print(response)
