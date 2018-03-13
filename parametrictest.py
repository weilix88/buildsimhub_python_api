import BuildSimHubAPI as bsh_api
import time

# 1. set your folder key
model_key = 'f9081a7f-4574-4e98-bb9e-3b77315ed49c'

bsh = bsh_api.BuildSimHubAPIClient()

new_pj = bsh.new_parametric_job(model_key)

# Define EEMs

wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.35, 0.3, 0.25]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2,0.9,0.6]
lpd.set_datalist(lpdValue)

coolCOP = bsh_api.measures.CoolingCOP()
cop = [2.80,2.86,3.0]
coolCOP.set_datalist(cop)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(coolCOP)

#Start!
new_pj.submit_parametric_study()

# track job progress
while (new_pj.track_simulation()):
    print(new_pj.get_status())
    time.sleep(5)
# Collect results
results = bsh.get_parametric_results(new_pj)

result_dict = results.net_site_eui()
result_unit = results.lastParameterUnit

# Plot
plot = bsh_api.postprocess.ParametricPlot(result_dict, result_unit)

plot.scatter_chart_plotly("Scatter plot demo")
plot.parallel_coordinate_plotly('LPD')

