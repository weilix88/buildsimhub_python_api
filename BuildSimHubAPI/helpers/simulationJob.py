import requests
import json
from .energyModel import Model

class SimulationJob():
    #every call will connect to this base URL
    BASE_URL = 'https://develop.buildsimhub.net/'

    def __init__(self, userKey, folderkey):
        self._userKey = userKey
        self._folderKey = folderkey
        self._trackToken = ""
        self._trackStatus = "No simulation is running or completed in this Job - please start simulation using createModel method."
        self._model = None

    @property
    def trackStatus(self):
        return self._trackStatus

    @property
    def model(self):
        return self._model

    def getSimulationResults(self, resultType="html"):
        if(self._trackToken == ""):
            return self._trackStatus

        url = SimulationJob.BASE_URL + 'GetSimulationResult_API'
        payload = {
            'user_api_key': self._userKey,
            'result_type': resultType,
            'track_token': self._trackToken
        }

        r = requests.post(url, params=payload, stream=True)

        f = ""
        if r.status_code == 200:
            f = r.text
        return f

    def trackSimulation(self):
        if(self._trackToken == ""):
            return self._trackStatus

        url = SimulationJob.BASE_URL + 'TrackSimulation_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._trackToken
        }
        r = requests.get(url, params=payload)
        resp_json = r.json()

        if(resp_json['has_more'] == True):
            self._trackStatus = resp_json['doing'] + " " + str(resp_json['percent']) + "%"
        else:
            self._trackStatus = "No simulation is running or completed in this Job - please start simulation using createModel method."

        return resp_json['has_more']

    def runSimulation(self, modelId, simulationType = "regular"):
        url = SimulationJob.BASE_URL + 'RunSimulation_API'
        payload = {
            'user_api_key': self._userkey,
            'track_token': modelId,
            'simulation_type': simulationType,
            'agents':agent
        }

        r = requests.post(url, data=payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            return resp_json['status']
        else:
            return resp_json['error_msg']


    def createModel(self, file_dir, comment = "Upload through Python API", simulationType ="", agent = 0):
        url = SimulationJob.BASE_URL + 'CreateModel_API'
        payload = {
            'user_api_key': self._userKey,
            'folder_api_key': self._folderKey,
            'comment': comment,
            'simulation_type': simulationType,
            'agents' : agent
        }

        files={
            'file': open(file_dir, 'rb')
        }

        r = requests.post(url, data=payload, files= files)

        resp_json = r.json()

        if(resp_json['status'] == 'success'):
            self._trackToken = resp_json['tracking']
            self._model = Model(self._userKey, self._trackToken)
            
            return resp_json['status']
        else:
            return resp_json['error_msg']

