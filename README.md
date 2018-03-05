[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sendgrid.svg?style=social&label=Follow)](https://twitter.com/buildsimhub)

**This library allows you to quickly and easily use the BuildSimHub Web API v1 via Python.**

This library represents the beginning of the Cloud Simulation function on BuildSimHub. We want this library to be community driven and BuildSimHub led. We need your help to realize this goal. To help, make sure we are building the right things in the right order, we ask that you create [issues](https://github.com/weilix88/buildsimhub_python_api/issues) and [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls) or simply upvote or comment on existing issues or pull requests.
We appreciate your continued support, thank you!

# Table of Contents
* [Installation](#installation)
* [Quick Start](#quick-start)
  * [SimulationType](#simultion_type)
  * [SimulationJob](#simulation_job)
  * [Model](#energy_model)
  * [HTML Parser](#eplus_html_parser)
* [Objects and Functions](#functions)
* [Roadmap](#roadmap)
* [About](#about)
* [License](#license)

<a name="installation"></a>

# Installation

## Prerequisites
- The BuildSimHub service, starting at the [free level](https://my.buildsim.io/register.html)
- Python version 3.4, 3.5 or 3.6

## Install Package
Simply clone this repository and place in any folder you wish to build your application on. Examples:
![picture alt](https://imgur.com/x60rk2O.png)

## Setup environment
After you downloaded the whole package, the first you need to do is to reconfigure your user API in the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config) file.
You can find the API key associate with your account under the profile page:

![picture alt](https://imgur.com/gHehDiN.png)

Simply add the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config)
`user_api_key:[YOUR_API_KEY]`

## Model key
The model key can be found under your buildsimhub project. After you set up a project on the platform, simply create an energy model in the project. You will then find the model key under the energy model tab (highlighted in the figure below)
![picture alt](https://imgur.com/gO4elTT.png)

<a name="quick-start"></a>

# Quick Start

## Run simulation
The following is the minimum needed code to initiate a regular simulation with the [helpers/simulationJob](https://github.com/weilix88/buildsimhub_python_api/tree/master/BuildSimHubAPI/helpers)

### With SimulationJob Class
```python
from BuildSimHubAPI import buildsimhub
#this key can be found under an energy model
model_key="0ade3a46-4d07-4b99-907f-0cfeec1072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"
###############NOW, START THE CODE########################

bsh = buildsimhub.BuildSimHubAPIClient()
newSJ = bsh.new_simulation_job(model_key)
response = newSj.run(file_dir,wea_dir)

############### WE DONE! #################################

#You can print the responses to verify whether the simulation
#is success or not.
print (response)
```
The `BuildSimHubAPIClient` creates a [portal object](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py) that manages simulation workflow.
From this object, you can initiate a [simulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) to conduct a cloud simulation. Call `run()` method with parameters can start the cloud simulation.

### Track Cloud simulation progress
```python
from BuildSimHubAPI import buildsimhub
bsh = buildsimhub.BuildSimHubAPIClient()

#this key can be found under your project folder
model_key="0ade3a46-4d07-4b99-907f-0cfee21072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

new_sj = bsh.new_simulation_job()
response = new_sj.run(file_dir,wea_dir)

######BELOW ARE THE CODE TO TRACK SIMULATION#########
if(response == 'success'):
  while new_sj.track_simulation():
    print (new_sj.trackStatus)
    time.sleep(5)
```
As mentioned previously, [BuildSimHubAPIClient](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py) manages the entire workflow of the simulation. So once a cloud simulation is successfully started by the [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) class, you can simply call `track_simulation()` function to receive the simulation progress.

### Retrieve Cloud simulation results
```python
from BuildSimHubAPI import buildsimhub
bsh = buildsimhub.BuildSimHubAPIClient()

#this key can be found under your project folder
model_key="0ade3a46-4d07-4b99-907f-0cfe321072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/USA_CO_Golden-NREL.724666_TMY3.epw"

new_sj = bsh.new_simulation_job()
response = new_sj.run(file_dir, wea_dir)

if(response == 'success'):
  while newSJ.track_simulation():
    print (newSJ.trackStatus)
    time.sleep(5)
  
  ######BELOW ARE THE CODE TO RETRIEVE SIMULATION RESULTS#########
  response = newSJ.get_simulation_results('html')
  print(response)
```
If the Job is completed, you can get results by calling `get_simulation_results(type)` function.

<a name="functions"></a>

#Object and Functions
<a name="simultion_type"></a>
## simulationType
[SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py) is a helper class that helps you configure the cloud simulation. Currently, there are only one simulation type available, which is `regular`. You can increase the number of agent by calling the `increase_agents()` function.
```python
simulationType = bsh.get_simulation_type()
num_of_agents = simulationType.increase_agents();
print (num_of_agents)
```
It should be noted that the maximum number of agents working on one simulation job is limited to 4, and the more agents you assigned to one simulation job, the faster your simulation can be. You can also call `reset_agent()` function to reset the number of agent to 1.

<a name="simulation_job"></a>
## SimulationJob
The easiest way to generate a [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) class is calling the `new_simulation_job()` method in the [BuildSimHubAPIClient](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py).
Nevertheless, you have to provide a `model_key` in order to create a new [SimulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) instance.

The `model_key` can be found under each folder of your project
![picture alt](https://imgur.com/jNrghIZ.png)

A simulation job manages one type of cloud simulation. It contains five main functions which are listed below:
### run
The `run()` function allows you to upload an energy model and weather file to the platform for cloud simulation (project creation is not required for this method). It has in total 2 parameters.
1. `file_dir` (required): the absolute local directory of your EnergyPlus / OpenStudio model (e.g., "/Users/weilixu/Desktop/5ZoneAirCooled.idf")
2. `wea_dir`(required): the absolute local director of the simulation weather file (it should be .epw file)

### create_model
The `create_model()` function allows you to upload an energy model to the platform with no simulation. It has in total 2 parameters.
1. `file_dir` (required): the absolute local directory of your EnergyPlus / OpenStudio model (e.g., "/Users/weilixu/Desktop/5ZoneAirCooled.idf")
2. `comment`(optional): The description of the model version that will be uploaded to your folder. The default message is `Upload through Python API`

This method returns two types of information:
If sucess: `success`
or error message states what was wrong in your request.

### create_run_model
The `create_run_model()` function allows you to upload an energy model to the platform and run simulaiton. It has in total 4 parameters.
1. `file_dir` (required): the absolute local directory of your EnergyPlus / OpenStudio model (e.g., "/Users/weilixu/Desktop/5ZoneAirCooled.idf")

2. `comment`(optional): The description of the model version that will be uploaded to your folder. The default message is `Upload through Python API`
3. `simulationType` (optional): The current available simulation tyoe is `regular`. This simulation Type can be generated from [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py) class. This class manages the simulation type as well as how many agents you want to assign to this simulation job. The default is `regular` for this class.

4. `agent` (optional): The agent numbeer should be selected among 1, 2 or 4 agents. You can also use the [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py) class to help decide the agent number. The more agents use for one simulation job, the faster this one simulation job can be finished. The default agent number is 1.

This method returns two types of information:
If sucess: `success`
or error message states what was wrong in your request.

### run_simulation
The `run_simulation()` function can be called inside a simulation job if the simulation is not conducted. The function has two parameters:
1. `simulationType` (optional): The simulation Type should be generated from [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py) class. This class manages the simulation type as well as how many agents you want to assign to this simulation job. The default is `regular`
2. `agent` (optional): he agent numbeer should be selected among 1, 2 or 4 agents. You can also use the [SimulationType](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationType.py) class to help decide the agent number. The more agents use for one simulation job, the faster this one simulation job can be finished. The default agent number is 1.

### track_simulaiton
The `track_simulation()` function does not require any parameters. However, it is required that a successful cloud simulation is created and running on the cloud. Otherwise, you will receive this message by calling this function:
`No simulation is running or completed in this Job - please start simulation using create_run_Model method.`
If there is a simulation running on the cloud for this simulationJob, then, this function will return `true` and you can retrieve the simulation status by get the class parameter `trackStatus`. Example code is below:
```python
if(newSimulationJob.track_simulation()):
  print(newSimulationJob.trackStatus)
```
### get_simulation_results
The `get_simulation_results(type)` function requires 1 parameter, the result type. Currently, you can retrieve three types of results: the error file (`err`), eso file (`eso`) and html file (`html`), generated from EnergyPlus simulation.

```python
response = newSimulationJob.get_simulation_results('err')
print (response)
```
<a name="energy_model"></a>
## Model
The model class contains a set of methods that provides the model information and results (after simulation). It can be generated from the `BuildSimHubAPIClient` with your specific simulation job. Here is an example to generate a model.

```python
bsh = buildsimhub.BuildSimHubAPIClient()
newSj = bsh.new_simulation_job(model_key)
model = bsh.get_model(newSj)
```

### Pre-simulation methods
1. *num_total_floor()*: can be called before simulation is completed. It returns the number of floors, or -1 if there is an error.
2. *num_zones()*: can be called before simulation is completed. It returns the total number of thermal zones, or -1 if there is an error.
3. *num_condition_zones()*: can be called before simulation is completed. It returns the total number of conditioned zones, or -1 if there is an error.
4. *conditioned_floor_area (unit)*: can be called before simulation is completed. It returns the floor areas of conditioned spaces, or -1 if there is an error. This method has an optional input: unit. If you wish to get ft2 unit, then you need to specify 'ip' for the unit parameter:
`  m.condition_floor_area("ip")
`
5. *gross_floor_area(unit)*: can be called before simulation is completed. It returns the total floor areas (including plenum spaces), or -1 if there is an error. This method has an optional input: unit. If you wish to get ft2 unit, then you need to specify 'ip' for the unit parameter:
`  m.gross_floor_area("ip")
`
6. *window_wall_ratio()*: can be called before simulation is completed. It returns the total window to wall ratio (above floor surface area) or -1 if there is an error.
7. *bldg_orientation()*: can be called before simulation is completed. It returns the orientation of the building.

### Post-simulation methods
1. *new_site_eui()*: It returns the net site eui of the simulation (includes generators such as PV). The unit should be based on model specification: SI (kWh/m2 or MJ/m2), IP(kWh/m2).
2. *total_site_eui()*: It returns the total site eui of the simulation. The unit should be based on model specification: SI (kWh/m2 or MJ/m2), IP(kWh/m2).
3. *not_met_hour_cooling()*: returns the time sepoint not met hours during cooling condition period. unit: hour
4. *not_met_hour_heating()*: returns the time sepoint not met hours during heating condition period. unit: hour
5. *not_met_hour_total()*: returns the time sepoint not met hours during heating and cooling condition period. unit: hour
6. *total_end_use_electricity()*: returns the total electricity consumption of the design. unit: kWh or GJ, IP is kBtu
7. *total_end_use_naturalgas()*: returns the total natural gas consumption of the design. unit: kWh or GJ, IP is kBtu
8. *cooling_electricity()*: returns the total electricity consumption of cooling energy. unit: kWh or GJ, Ip is kBtu
9. *domestic_hotwater_electricity()*: returns the total electricity consumption of the service water system. unit: kWh or GJ, IP is kBtu
10. *domestic_hotwater_naturalgas()*: returns the total natural gas consumption of the service water system. unit: kWh or GJ, IP is kBtu
11. *exterior_equipment_electricity()*: returns the total electricity consumption of the exterior equipment. unit: kWh or GJ, IP is kBtu
12. *exterior_equipment_naturalgas()*: returns the total natural gas consumption of the exteiror equipment. unit: kWh or GJ, IP is kBtu
13. *exterior_lighting_electricity()*: returns the total electricity consumption of the exterior lighting system. unit: kWh or GJ, IP is kBtu
14. *exterior_lighting_naturalgas()*: returns the total natural gas consumption of the exterior lighting system. unit: kWh or GJ, IP is kBtu
15. *fan_electricity()*: returns the total electricity consumption of the fan system. unit: kWh or GJ, IP is kBtu
16. *heating_electricity()*: returns the total electricity consumption of the heating system. unit: kWh or GJ, IP is kBtu
17. *heating_naturalgas()*: returns the total natural gas consumption of the heating system. unit: kWh or GJ, IP is kBtu
18. *heat_rejection_electricity()*: returns the electricity consumption of the heat rejection. unit: kWh or GJ, IP is kBtu
19. *heat_rejection_naturalgas()*: returns the natural gas consumption of the heat rejection. unit: kWh or GJ, IP is kBtu
20. *interior_equipment_electricity()*: returns the electricity consumption of the interior equipment. unit: kWh or GJ, IP is kBtu
21. *interior_equipment_naturalgas()*: returns the natural gas consumption of the interior equipment. unit: kWh or GJ, IP is kBtu
22. *interior_lighting_electricity()*: returns the electricity consumption of the interior lighting. unit: kWh or GJ, IP is kBtu
23. *interior_lighting_naturalgas()*: returns the natural gas consumption of the interior lighting. unit: kWh or GJ, IP is kBtu
24. *pumps_electricity()*: returns the electricity consumption of the pumps. unit: kWh or GJ, IP is kBtu
25. *pumps_naturalgas()*: returns the natural gas consumption of the pumps. unit: kWh or GJ, IP is kBtu

### Misc. methods and variables
1. lastParameterUnit: You can check the value of the variable requested by the most recent API call.
```python
m = new_sj.model
print(str(m.net_site_eui())+ " " + m.lastParameterUnit)
#Output: 242.98 MJ/m2
print(str(m.total_end_use_electricity())+ " " + m.lastParameterUnit)
#Output: 156.67 GJ
```
<a name = "eplus_html_parser"></a>
## eplusHTMLParser
The eplusHTMLParser provides a set of methods to help users finding data in the EnergyPlus HTML output file. To use this HTML parser, user has to retrieve the processed HTML file from BuildSimHub service. An example code is illustrated below.
```python
from BuildSimHubAPI import eplusHTMLParser
...
  response = new_sj.get_simulation_results('html')
  value_dict = eplusHTMLParser.extract_a_value_from_table(response, 'Annual Building Utility Performance Summary',
    'Site and Source Energy', 'Energy Per Total Building Area', 'Net Site Energy')
  print(value_dict['value] + " " + value_dict['unit'])
  
  #Output: 241.7 MJ/m2
```
### extract_a_value_from_table(report, table, column_name, row_name, reportFor)
This method allows users to extract a specifc cell value from HTML file. It has four required parameters and one optional parameter.
1. `report`: the name of the report in the HTML file. You can find the list of available reports under the Table of Content section in the HTML file.
![picture alt](https://imgur.com/QEB5XXF.png)
2. `table`: the name of the table in the HTML file. You can find the table name under each report. Figure below shows an example of the table name:
![picture alt](https://imgur.com/MYRODca.png)
3. `column_name`: the header of a column which the cell is located in. The header may contains unit, but you do not need to include the unit for this parameter.
![picture alt](https://imgur.com/PTcgcC5.png)
4. `row_name`: the name of the row, typically starts at the first column of a table. The row name may contains unit, but you do not need to include the unit for this parameter.
![picture alt](https://imgur.com/UY3CHPR.png)
5. `reportFor`: This is an optional parameter. The default is set to 'Entire Facility'. Usually, all the report is for entire facility. However, there are some cases where the report is generated for a specific zone, e.g., zone load component reports. Below is the example of finding this parameter in the HTML file.
![picture alt](https://imgur.com/ZiCyT68.png)

<a name="roadmap"></a>
# Roadmap
1. We are also working on APIs for results retrieving, which let users to get simulation results for post-processing.
2. If you are interested in the future direction of this project, please take a look at our open [issues](https://github.com/weilix88/buildsimhub_python_api/issues) and [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls). We would love to hear your feedback.


<a name="about"></a>
# About

buildsimhub-python is guided and supported by the BuildSimHub [Developer Experience Team](mailto:haopeng.wang@buildsimhub.net).

buildsimhub-python is maintained and funded by the BuildSimHub, Inc. The names and logos for buildsimhub-python are trademarks of BuildSimHub, Inc.

<a name="license"></a>
# License
[The MIT License (MIT)](LICENSE.txt)

