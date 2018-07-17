"""
This example demonstrates how to ask BuildSim Cloud to automatically update the design day
data for an uploaded model to the same location as its weather file.

Also, it demonstrates how to get the ASHRAE Appendix G specified (Heating 99% cooling 1%) design day
conditions from a model
"""
import BuildSimHubAPI as bshapi

file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
wea_dir_sf = "/Users/weilixu/Desktop/data/UnitTest/insf.epw"


# model_key can be found in each model information bar
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'

bsh = bshapi.BuildSimHubAPIClient()

new_sj = bsh.new_simulation_job(project_customized_key)
model = new_sj.run(file_dir, wea_dir_sf, design_condition='yes', track=True)
design_info = model.get_design_day_condition()
print(design_info['cooling'])
print(design_info['heating'])
print(design_info['site'])
