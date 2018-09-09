"""
Author: Weili Xu

"""
import time

import BuildSimHubAPI as bsh_api
import pandas as pd
import numpy as np
from sklearn import linear_model
import scipy.optimize as opt

# 1. set your folder key
project_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
model_api_key = '17596d44-4126-44d1-b347-e8fd78a6fb9a'
local_file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
number_of_simulation = 100
budget = 220000


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


def window_wall_ratio_cost(val):
    return -13143.2 * val + 33255.32


def wall_r_cost(val):
    return 432 * val + 11230.2


def lpd_cost(val):
    return -8112 * val + 19885.4


def chiller_cost(val):
    return 8732.2 * val + 23222.22


def boiler_cost(val):
    return 9174.44 * val + 17837.99


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


# Start script
start = time.time()
print("Start the Script!")
print("#############################################################")
bsh = bsh_api.BuildSimHubAPIClient()
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

results = bsh.parametric_results(project_key, model_api_key)

# Get the EUI results
# Collect results
print("Extracting data from cloud....")
print("#############################################################")
result_dict = results.net_site_eui()
result_unit = results.last_parameter_unit
print("Finish extracting data from cloud...")
print("#############################################################")

print()
print()
print("Start training a model...")
print("#############################################################")
df = convert_parajson_pandas(result_dict)
print(df.to_string())
print(df.loc[df['value'].idxmin()])
# Training code starts from here
y = df.loc[:, 'value']
x = df.loc[:, df.columns != 'value']
column_head = list(x)
# train a regression model
alg = linear_model.LinearRegression()
alg.fit(x, y)

print("Model training a completed!...")
print('Interpret value β0: '+str(alg.intercept_))
print('training score: ' + str(alg.score(x, y)))
print('Linear regression model: ' + str(alg.intercept_) + ' + ' + pretty_print_linear(alg.coef_))
print("#############################################################")

# OPTIMIZATION FUNCTIONS
# obj function
end = time.time()
print("Start optimization: " + str(end - start))
print("#############################################################")


def fun(x_pred): return alg.predict([x_pred])


# constraint function
def cost(x_pred):
    cost = 0.0
    for i in range(len(column_head)):
        head = column_head[i].strip()
        if head == 'Wall_R':
            cost += wall_r_cost(x_pred[i])
        elif head == 'LPD':
            cost += lpd_cost(x_pred[i])
        elif head == 'ChillerCOP':
            cost += chiller_cost(x_pred[i])
        elif head == 'HeatingEff':
            cost += boiler_cost(x_pred[i])
        else:
            cost += window_wall_ratio_cost(x_pred[i])
    return budget - cost


boundary = [bounds(col_head) for col_head in column_head]
X = np.array([[col_max(col_head)] for col_head in column_head])
X.reshape(1, -1)
res = opt.minimize(fun, X, bounds=boundary, options={'disp': True}, constraints={'type': 'ineq', 'fun': cost})

print()
end = time.time()
print("#############################################################")
print("Optimization completed in : " + str(end - start) + " seconds")

print("Optimized")
print(column_head)
print(res.x)

target_val = alg.predict([res.x])
total_cost = budget - cost(res.x)
print('Predicted EUI: ' + str(target_val) + ' kBtu/ft2')
print('Cost: $' + str(total_cost) + ' compare to budget: $' + str(budget))
