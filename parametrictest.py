import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()

# 1. set your folder key
model_key = 'a0bc8633-d300-4d80-8f89-9351d992b868'
# 2. define the absolute directory of your energy model
# file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
# model_key_list = ['a', 'b', 'c']
# 3. this is optional
new_pj = bsh.new_parametric_job(model_key)

# add window property
# wp = bshapi.measures.WindowUValue()
# uValue = [2.2, 1.6, 1.4]
# wp.set_datalist(uValue)

# wshgc = bshapi.measures.WindowSHGC()
# shgc = [0.4, 0.3, 0.2]
# wshgc.set_datalist(shgc)

# wrr = bshapi.measures.WindowWallRatio()
# win = [0.2, 0.3]
# wrr.set_datalist(win)

wr = bshapi.measures.WallRValue()
rValue = [2.3, 3.5]
wr.set_datalist(rValue)

rr = bshapi.measures.RoofRValue()
rrValue = [3.1, 3.5, 4.0]
rr.set_datalist(rrValue)

lpd = bshapi.measures.LightLPD()
lpdValue = [8.1, 6.5, 4.3]
lpd.set_datalist(lpdValue)

infiltration = bshapi.measures.Infiltration()

occupancy = bshapi.measures.OccupancySensor()

# add these EEM to parametric study
#new_pj.add_model_measure(wp)
#new_pj.add_model_measure(wshgc)
#new_pj.add_model_measure(wrr)
new_pj.add_model_measure(wr)
new_pj.add_model_measure(rr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(infiltration)
new_pj.add_model_measure(occupancy)

# estimate runs and submit job
# print(newPj.num_total_combination())
print(new_pj.submit_parametric_study())
print(new_pj.trackToken)

# track job progress
while (new_pj.track_simulation()):
    print(new_pj.get_status())
    time.sleep(5)

# collect job results
results = bsh.get_parametric_results(new_pj)

result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit

# plot
plot = bshapi.postprocess.ParametricPlot(result_dict, result_unit)

plot.line_plot("this is demo for line plot")
plot.parallel_coordinate("this is demo for parallel coordinate plot", "Window_U")
