from BuildSimHubAPI import buildsimhub
from BuildSimHubAPI import eplusHTMLParser
import time

bsh = buildsimhub.BuildSimHubAPIClient()

#1. set your folder key
model_key="0dde5a46-4d07-4b99-907f-0cfedf301072"
#2. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
#3. this is optional

newSj = bsh.new_simulation_job(model_key)
#5. start the API call
# note if fast simulation, call increaseAgents to increase the agent numbers
response = newSj.create_run_model(file_dir)
if(response == 'success'):
  while newSj.track_simulation():
    print (newSj.trackStatus)
    time.sleep(5)

  response = newSj.get_simulation_results('html')
  value_dict = eplusHTMLParser.extract_a_value_from_table(response, 'Annual Building Utility Performance Summary',
    'Site and Source Energy', 'Energy Per Total Building Area', 'Net Site Energy')

  print(value_dict['value'] + " " + value_dict['unit'])
else:
  print(response)
