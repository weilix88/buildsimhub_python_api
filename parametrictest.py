import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()

# 1. set your folder key
model_key = '6b2c778c-f795-4444-a2c7-fc614efdb66b'
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

wrr = bshapi.measures.WindowWallRatio()
win = [0.35, 0.3, 0.25]
wrr.set_datalist(win)

lpd = bshapi.measures.LightLPD('ip')
lpdValue = [1.2,0.9,0.6]
lpd.set_datalist(lpdValue)

coolCOP = bshapi.measures.CoolingCOP()
# 2.80 07, 10 aircooled chiller efficiency
# 2.866 ashrae
# 3.0 50% savings for med-small office-aircooled chiller
cop = [2.80, 2.86, 3.0]
coolCOP.set_datalist(cop)

# add these EEM to parametric study
#new_pj.add_model_measure(wp)
#new_pj.add_model_measure(wshgc)
#new_pj.add_model_measure(wrr)
new_pj.add_model_measure(wrr)
#new_pj.add_model_measure(rr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(coolCOP)
#new_pj.add_model_measure(occupancy)

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
plot.parallel_coordinate_plotly()
