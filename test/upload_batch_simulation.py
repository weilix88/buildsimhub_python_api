"""
This sample file demonstrate how to upload a list of EnergyPlus models into one simulation job

Current issue the tracking will skip the first model, so user might see a  model missing in the tracking information.
e.g.
Upload 2 models and run them in parallel
But tracking info shows:
Total progress 0%, success: 0, failure: 0, running: 1, queue: 0

This is a known issue and we will working on a fix solution.

"""

import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp

# project_key can be found in every project (click the information icon next to project name)
project_key = "9d6b010f-de6f-4f18-9030-411467288b11"

file_dir_1 = "/Users/weilixu/Desktop/data/doasfancoil.idf"
file_dir_2 = "/Users/weilixu/Desktop/data/mediumoffice.idf"
# initialize the client
bsh = bsh_api.BuildSimHubAPIClient()

"""
The most straightforward way to do simulation
"""
new_sj_run = bsh.new_simulation_job(project_key)
results = new_sj_run.run([file_dir_1, file_dir_2], track=True)

