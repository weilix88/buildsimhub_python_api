[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)
[![Twitter Follow](https://img.shields.io/twitter/follow/sendgrid.svg?style=social&label=Follow)](https://twitter.com/buildsimhub)

**This library allows you to quickly and easily use the BuildSimHub Web API v1 via Python.**

This library represents the beginning of the Cloud Simulation function on BuildSimHub. We want this library to be community driven and BuildSimHub led. We need your help to realize this goal. To help, make sure we are building the right things in the right order, we ask that you create [issues](https://github.com/weilix88/buildsimhub_python_api/issues) and [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls) or simply upvote or comment on existing issues or pull requests.
We appreciate your continued support, thank you!

For more information, examples, and tutorials, please check our [wiki page](https://github.com/weilix88/buildsimhub_python_api/wiki).

# Table of Contents
* [Latest Update](#update)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [Roadmap](#roadmap)
* [About](#about)
* [License](#license)

<a name="update"></a>
Latest Version 1.6.0:
1. EplusGIT model management system - compare, merge and copy - can be accessed through API
2. Regional project and global project. - the newly added global project allows user upload custom weather files for simulation / parametrics.
3. Design day condition - automatically update design day conditions.

Previous update:
Version 1.5.5:
4. Package and distribution on PYPI
5. New [monte carlo] algorithm is implemented in parametric study.
6. New methods to modify energy efficiency measure and parameters in a single model.

Version 1.5.0:
7. API library is now supporting model download. Check out this [script](https://github.com/weilix88/buildsimhub_python_api/blob/master/test/download_model_test.py)
8. Model upload support customize (.CSV) schedules. Check out this [script](https://github.com/weilix88/buildsimhub_python_api/blob/master/test/simulation_csv_test.py)
9. Supports hourly data extract from a single model. [script](https://github.com/weilix88/buildsimhub_python_api/blob/master/test/hourly_data_retrieve.py)
10. Support extracting a single table from HTML. [script](https://github.com/weilix88/buildsimhub_python_api/blob/master/test/html_table_test.py)
11. Open 3D geometry viewer using API. [script](https://github.com/weilix88/buildsimhub_python_api/blob/master/test/model_geo_test.py)
12. Zone Load / Load component Extraction. [script](https://github.com/weilix88/buildsimhub_python_api/blob/master/test/zone_load_test.py)
13. Add post-processing functions - convert data to pandas dataframe, and utilize plotly for plotting.

Version 1.4.0
14. Initialize a simulation job / parametric job requires a project api key now.
15. User API key is deleted
16. Run function in simulation job supports multiple models submission.
17. Include more standard measures: Building orientation, overhangs, fins, roof absorptions, water heater, water usage, equipment power
18. Include more data retriving options at building level.

<a name="installation"></a>

# Installation

## Prerequisites
- The BuildSimHub service, starting at the [free level](https://my.buildsim.io/register.html)
- Python version 3.5 or 3.6, Python 2.7 is under-testing.
- If you wish to use the Built-in plotting function, you will then need the latest Plotly python package. The installation instruction can be found in [here](https://plot.ly/python/getting-started/)

## Install Package
```
pip install BuildSimHubAPI
```

## Setup environment
There are no requirements for regular users to access BuildSim Cloud besides a Python installation.
However, for software vendors who would like to integrate the BuildSim Cloud, you can revise the vendor key in the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config) file.

Edit the [info.config](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/info.config)
`vendor_id:[Your name]`
If you decided to use BuildSim Cloud, please send your specific vendor id to us: weili.xu@buildsimhub.net.

## Project key (required)
To activate a simulation through API client, you need to supply a project key - a key that helps BuildSim connect your local application to your project.
The project key can be found in two places.
1. Project list page: Simply click the "Copy Key" button and paste it in you application.
![picture alt](https://imgur.com/61cyNlE.png)
2. In the project tab under every model: Under every model, search for project api key field in the project tab.
![picture alt](https://imgur.com/hndWwBI.png)

```python
'''
Example of how to innitialize API client
'''
project_api_key = 'abcdef-ghijkl-mnopqrst'
bsh = buildsimhub.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job(project_api_key)
```

## Model key (optional)
Some functions in the API library requires you to supply a `model_api_key`. These functions allow you to update a model's history or retrieve the simulation results from a model under the specified project. The `model_api_key` can be found in every model (highlighted in the figure below).
![picture alt](https://imgur.com/gO4elTT.png)

<a name="quick-start"></a>
# Quick Start
### Hello BuildSim
```python
from BuildSimHubAPI import buildsimhub
###############NOW, START THE CODE########################

bsh = buildsimhub.BuildSimHubAPIClient()
new_sj = bsh.new_simulation_job('abcdef-ghijkl-mnopqrst')
model = new_sj.run("/Users/weilixu/Desktop/5ZoneAirCooled.idf", track=True)

print(model.net_site_eui())
```

The `BuildSimHubAPIClient` creates a [portal object](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/buildsimhub.py) that manages simulation workflow.
From this object, you can initiate a [simulationJob](https://github.com/weilix88/buildsimhub_python_api/blob/master/BuildSimHubAPI/helpers/simulationJob.py) to conduct a cloud simulation. Call `run()` method with parameters can start the cloud simulation. The returned object is the [model object](https://github.com/weilix88/buildsimhub_python_api/wiki/Simulation_Results), which contains full set of simulation results.

### Quick start for Parametric simulation
```python
import BuildSimHubAPI as bsh_api
project_api_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_api_key) 
 
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
parametric = new_pj.submit_parametric_study_local(file_dir, algorithm='montecarlo', size=10, track=True)  

print(parametric.net_site_eui())
```
The parametric workflow requires user specified energy efficient measures. The full list of measures can be found in [BuildSimHub wiki](https://github.com/weilix88/buildsimhub_python_api/wiki/Parametric#energyefficientmeasures).

<a name="roadmap"></a>
# Roadmap
1. We are working on a standard EEMs, which allows user to apply common energy efficiency measures to any IDF models. Open an issue if you did not see any desired EEMs in the standard EEM library!
2. More simulation configurations and output results return will be added in the future!
3. BuildSim Plot: This is the new project which we are integrating plotly package with our standard API library to provide the capability of visualizations.
4. BuildSim Learn: This is a new project which we are working on integrating scikit-learn into the current workflow to enhance the parametric workflow.
5. If you are interested in the future direction of this project, please take a look at our open [issues](https://github.com/weilix88/buildsimhub_python_api/issues) and [pull requests](https://github.com/weilix88/buildsimhub_python_api/pulls). We would love to hear your feedback.

<a name="about"></a>
# About

buildsimhub-python is guided and supported by the BuildSimHub [Developer Experience Team](mailto:haopeng.wang@buildsimhub.net).

buildsimhub-python is maintained and funded by the BuildSimHub, Inc. The names and logos for buildsimhub-python are trademarks of BuildSimHub, Inc.

<a name="license"></a>
# License
[The MIT License (MIT)](LICENSE.txt)
