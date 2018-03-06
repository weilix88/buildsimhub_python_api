import BuildSimHubAPI as bshapi
import matplotlib.pyplot as plt
import numpy as np
import time

bsh = bshapi.BuildSimHubAPIClient()

# 1. set your folder key
model_key = 'ec76b257-5dc2-470a-846e-b8894597530d'
# 2. define the absolute directory of your energy model
# file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
model_key_list = ['a', 'b', 'c']
# 3. this is optional
newPj = bsh.new_parametric_job(model_key)

# add window property
wp = bshapi.measures.WindowUValue()
uValue = [2.0, 1.6, 1.4]
wp.set_datalist(uValue)

wshgc = bshapi.measures.WindowSHGC()
shgc = [0.5, 0.4, 0.3]
wshgc.set_datalist(shgc)

wrr = bshapi.measures.WindowWallRatio()
win = [0.2, 0.3]
wrr.set_datalist(win)

# add these EEM to parametric study
newPj.add_model_measures(wp)
newPj.add_model_measures(wshgc)
# newPj.add_model_action(wwr)

# estimate runs and submit job
# print(newPj.num_total_combination())
newPj.submit_parametric_study()
print(newPj.trackToken)

# track job progress
while (newPj.track_simulation()):
    print(newPj.get_status())
    time.sleep(5)

# collect job results
results = bsh.get_parametric_results(newPj)

result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit

# plot
plot = bshapi.postprocess.ParametricPlot(result_dict, result_unit)

plot.line_plot("this is demo for line plot")
plot.parallel_coordinate("this is demo for parallel coordinate plot")
