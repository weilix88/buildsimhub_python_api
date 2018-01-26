[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sendgrid.svg?style=social&label=Follow)](https://twitter.com/buildsimhub)

**This library allows you to quickly and easily use the BuildSimHub Web API v1 via Python.**
This library represents the beginning of the Cloud Simulation function on BuildSimHub. Please browse the rest of this README for further detail.
We appreciate your continued support, thank you!

# Table of Contents
* [Installation](#installation)
* [Quick Start](#quick-start)

<a name="installation"></a>
# Installation

## Prerequisites
- The BuildSimHub service, starting at the [free level](https://my.buildsim.io/register.html)
- Python version 2.6, 2.7, 3.4, 3.5 or 3.6

## Install Package
Simply clone this repository and place in any folder you wish to build your application on. Examples:
![picture alt](https://imgur.com/x60rk2O.png)

## Setup environment
After you downloaded the whole package, the first you need to do is to reconfigure your user API in the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config) file.
You can find the API key associate with your account under the profile page:

![picture alt](https://imgur.com/gHehDiN.png)

Simple edit the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config)
`user_api_key:[YOUR_API_KEY]`

<a name="quick-start"></a>
# Quick Start

## Run simulation
The following is the minimum needed code to initiate a regular simulation with the [helpers/simulationJob](https://github.com/weilix88/buildsimhub_python_api/tree/master/BuildSimHubAPI/helpers)

### With SimulationJob Class
```python
from BuildSimHubAPI import buildsimhub
bsh = buildsimhub.BuildSimHubAPIClient()

#this key can be found under your project folder
folder_key="0ade3a46-4d07-4b99-907f-0cfeece321072"

#absolute directory to the energyplus model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"

newSJ = bsh.newSimulationJob(folder_key)
response = newSj.createModel(file_dir)

#print success means the simulation job has successfully
#started a simulation, if there is an error, then
#you will receive the correspondent error message
print (response)
```
The `BuildSimHubAPIClient` creates a [portal object](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py) that manages simulation workflow.
From this object, you can initiate a [simulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) to conduct a cloud simulation. Call `createModel()` method with parameters can start the cloud simulation.

