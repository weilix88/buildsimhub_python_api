"""
Author: Weili Xu
"""

import BuildSimHubAPI as bsh_api
import pandas as pd
import numpy as np
from sklearn import linear_model
import scipy.optimize as opt

# 1. set your folder key
project_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = ''
local_file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
number_of_simulation = 100


# Helper functions
# A helper method for pretty-printing linear models
def pretty_print_linear(coefs, names=None, sort=False):
    if names is None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)
    if sort:
        lst = sorted(lst, key=lambda x: -np.abs(x[0]))
    return " + ".join("%s * %s" % (round(coef, 3), name)
                      for coef, name in lst)


def convert_parajson_pandas(result_dict):
    for i in range(len(result_dict)):
        tempstr = result_dict["value"]

    dict = {}
    for key in result_dict:
        if key == "model":
            templist = result_dict[key]
            tempdict = {}
            for i in range(len(templist)):
                tempstr = result_dict["model"][i]
                templist = tempstr.split(',')
                for j in range(len(templist)):
                    pair = templist[j].split(': ')
                    if pair[0] not in tempdict:
                        tempdict[pair[0]] = []
                    tempdict[pair[0]].append(pair[1])
            for subkey in tempdict:
                dict[subkey] = tempdict[subkey]
        elif key != 'model_plot':
            dict[key] = result_dict[key]
    return pd.DataFrame(dict)


def bounds(col_head):
    col_head = col_head.strip()
    for measure in measure_list:
        if measure.measure_name == col_head:
            return measure.get_boundary()


def col_max(col_head):
    col_head = col_head.strip()
    for measure in measure_list:
        if measure.measure_name == col_head:
            return measure.get_max()


bsh = bsh_api.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
# if the seed model is on the buildsim cloud - add model_api_key to the new_parametric_job function
new_pj = bsh.new_parametric_job(project_key)

# Define EEMs
measure_list = list()

wwrn = bsh_api.measures.WindowWallRatio(orientation="N")
wwrn.set_min(0.3)
wwrn.set_max(0.6)
measure_list.append(wwrn)

wwrs = bsh_api.measures.WindowWallRatio(orientation="S")
wwrs.set_min(0.3)
wwrs.set_max(0.6)
measure_list.append(wwrs)

wwrw = bsh_api.measures.WindowWallRatio(orientation="W")
wwrw.set_min(0.3)
wwrw.set_max(0.6)
measure_list.append(wwrw)

wwre = bsh_api.measures.WindowWallRatio(orientation="E")
wwre.set_min(0.3)
wwre.set_max(0.6)
measure_list.append(wwre)

wallr = bsh_api.measures.WallRValue('ip')
wallr.set_min(20)
wallr.set_max(40)
measure_list.append(wallr)

lpd = bsh_api.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
measure_list.append(lpd)

chillerEff = bsh_api.measures.CoolingChillerCOP()
chillerEff.set_min(3.5)
chillerEff.set_max(5.5)
measure_list.append(chillerEff)

heatEff = bsh_api.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

# Add EEMs to parametric job
new_pj.add_model_measures(measure_list)

results = None
# Start!
if model_api_key is not None and model_api_key != '':
    results = new_pj.submit_parametric_study(model_api_key=model_api_key, algorithm='montecarlo',
                                             size=number_of_simulation, track=True)
elif local_file_dir is not None and local_file_dir != '':
    results = new_pj.submit_parametric_study_local(local_file_dir, algorithm='montecarlo', size=number_of_simulation,
                                                   track=True)
# Get the EUI results
# Collect results
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit

df = convert_parajson_pandas(result_dict)
# Training code starts from here
y = df.loc[:, 'value']
x = df.loc[:, df.columns != 'value']
column_head = list(x)
# train a regression model
alg = linear_model.LinearRegression()
alg.fit(x, y)
print('Interpret value β0: '+str(alg.intercept_))
print('training score: ' + str(alg.score(x, y)))
print('Linear regression model: ' + str(alg.intercept_) + ' + ' + pretty_print_linear(alg.coef_))


def fun(x_pred): return alg.predict([x_pred])


bounds = [bounds(col_head) for col_head in column_head]
X = np.array([[col_max(col_head)] for col_head in column_head])
X.reshape(1, -1)
res = opt.minimize(fun, X, bounds=bounds, options={'disp': True})

print("Optimized")
print(column_head)
print(res.x)

target_val = alg.predict([res.x])
print(target_val)

