# BuildSim Plot

## Introduction
BuildSim Plot is the first project we launched after the release of BuildSimHub API library. Often time, we saw engineers spend numerous time compiling thousands of simulation data, struggling with the content and plots that can barely cover their innovative explorations. Sometime, the report may produce more questions from the client.

We want to help engineers and architects to communicate their ideas and discoveries in a simple way. We believe a good plot should speak for itself. So that is the reason we started our BuildSim Plot project.

Every script under the BuildSim Plot project is open-source, which means they are free for downloading. If you are a BuildSim Cloud user, you can take any of those scripts to create your unique plot in a second! Best of all, those plots are shareable and interactive, which makes it super-easy to understand.

We also encourage engineers and architects to share their scripts under the BuildSim Plot project. Together, we can produce so many amazing plots, help the industry become more efficient and save your time to do more work that you truly loves.

## How to use the scripts:
Open a script, for instance, the `zone_load_plot.py`, the first thing is to read the python doc carefully:
```python
"""
AUTHOR: Weili Xu
DATE: 6/28/2018

WHAT IS THE SCRIPT ABOUT?
This script demonstrates how to zone load data in a building and how to plot the load data in a bar chart

HOW TO USE THE SCRIPT?
Replace the project_api_key and model_api_key with your model

PACKAGE REQUIRED:
Pandas, Plotly

"""

```
The first two indicates who wrote this script and when this script was accepted to publish on the BuildSim Plot project.
* Following by the first question: `What is the script about?` . This gives quick overview about this script: why it is produced, what type of analysis you can do with it etc.

* Secondly, `How to use the script?` described how a user should use this script to make beautiful plots

* Lastly, `Package required` indicates what packages a user should install with their python before running this script.

That's it! Once you read this part, you should be good to go now!
## Latest update:
Sankey chart plot the zone load components in zone_load_component_sankey.py.

## How to contribute
If you are a BuildSim Cloud user and you want to contribute to this project, you can follow the procedure below:
1. Fork the BuildSimHubAPI library project from our [Github repository](https://github.com/weilix88/buildsimhub_python_api)
2. In your local github repository, make a copy the [buildsimhub_python_api.py](https://github.com/weilix88/buildsimhub_python_api/blob/master/buildsimplot/buildsim_plot_template.py) and rename it with any name you like.
3. Follow the template in the python and insert your code.
4. Create a pull request with the request message: BuildSimPlot - [xxxx - your file name goes here]
