import BuildSimHubAPI as bshapi
import time

bsh = bshapi.BuildSimHubAPIClient()

#1. set your folder key
model_key="0dde5a46-4d07-4b99-907f-0cfedf301072"
#2. define the absolute directory of your energy model
file_dir = "/Users/weilixu/Desktop/5ZoneAirCooled.idf"
#3. this is optional

newPj = bsh.new_parametric_job(model_key)

#add window property
wp = bshapi.actions.WindowUValue('ip')
uValue = [0.3,0.2,0.1]
wp.set_datalist(uValue)

wshgc = bshapi.actions.WindowSHGC()
shgc = [0.3,0.4,0.5]
wshgc.set_datalist(shgc)

#add window wall ratio property
wwr = bshapi.actions.WindowWallRatio()
wwrlist = [0.2,0.3,0.4]
wwr.set_datalist(wwrlist)

#add these EEM to parametric study
newPj.add_model_action(wp)
newPj.add_model_action(wshgc)
newPj.add_model_action(wwr)

#estimate runs
print(newPj.num_total_combination())

print(newPj.submit_parametric_study_local(''))