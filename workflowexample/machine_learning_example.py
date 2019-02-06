from BuildSimHubAPI.mlengine import *

# first user inputs
project_api_key = '6e764740-cb49-40ed-8a1a-1331b1d87ed2'
model_api_key = 'c29f5b91-ae6b-43dc-bbf3-31b64ac70e78'

# STEP1: retrieve enum list (defined by user)
request_data_list = [e.name for e in RequestData]
# send this to user for display
print(request_data_list)

# STEP1.1: set enum for data
# receive the user selected data
select_enum_list = ['bldg_heat_load', 'bldg_cool_load']
request_list = []
for s in select_enum_list:
    request_list.append(RequestData[s])
# STEP2: Request data from BuildSim Cloud
dr = DataRequester()
# STEP2.1: Data pre-processing
dr.retrieve_data(project_api_key, model_api_key, RequestData.net_site_eui,
                 base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

# user operations: flip catgorical data to numeric data
dr.set_datatype_num(['WWR'])

# STEP3: Train model
# Model selection & feature selections
# Training
df = dr.get_df()
print(df.to_string())
headers = list(df)
rf = SVRLinear(df)
# auto-tune values
rf.grid_search_cv(headers[-1])

print(rf.hyper_parameter_spec())
print(rf.train(headers[-1]))
print(rf.get_feature_list())

# STEP4: prediction based on values
val_dict = dict()
val_dict['WWR'] = [0.2]
val_dict['DaylitSensor'] = ['On']
val_dict['HVAC'] = ['doaswshp']

print(rf.predict(val_dict))
