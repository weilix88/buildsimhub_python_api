import requests
import json

class ParametricJob():
    #every call will connect to this base URL
    BASE_URL = 'https://develop.buildsimhub.net/'

    def __init__(self, userKey, mk):
        self._userKey = userKey
        self._modelKey = mk
        #list of data
        self._simulation_job = list()
        self._model_action_list = list()

    def add_model_action(self, action):
        self._model_action_list.append(action)

    def num_total_combination(self):
        num_total = 0
        for i in range(len(self._model_action_list)):
            if(num_total == 0):
                num_total = self._model_action_list[i].get_num_value()
            else:
                num_total = num_total * self._model_action_list[i].get_num_value()
        return num_total

    def submission_cost(self, file_dir):
        #reserved function
        return num_total_combination() * 1.0

    #For this method, it allows user to upload energy model from local machine, along with the weather file
    #this will creates a new project each time and run the parametric simulation.
    def submit_parametric_study_local(self, file_dir, wea_dir, simulationType ="parametric", agent = 1):
        #file_dir indicates the seed model
        url = ParametricJob.BASE_URL + 'CreateModel_API'
        payload = {
            'user_api_key': self._userKey,
            'simulation_type': simulationType,
            'agents':agent
        }

        for i in range(len(self._model_action_list)):
            action = self._model_action_list[i]
            payload[action.get_api_name()] = action.get_datalist()

        files = {
            'file': open(file_dir, 'rb')
        }

        r = requests.post(url, data=payload, files= files)

        resp_json = r.json()

        if(resp_json['status'] == 'success'):
            self._trackToken = resp_json['tracking']
            return resp_json['status']
        else:
            return resp_json['error_msg']

    #for this method, it allows user to identify one seed model in a project.
    #This allows the parametric study performed under a project with fixed weather file,
    def submit_parametric_study(self, seed_model_key, simulationType = 'parametric', agent = 1):

        url = ParametricJob.BASE_URL + ''
        payload = {
            'user_api_key': self._userKey,
            'simulation_type': simulationType,
            'agents':agent
        }

        for i in range(len(self._model_action_list)):
            action = self._model_action_list[i]
            payload[action.get_api_name()] = action.get_datalist()

        r = requests.post(url, data=payload, files= files)

        resp_json = r.json()

        if(resp_json['status'] == 'success'):
            self._trackToken = resp_json['tracking']
            return resp_json['status']
        else:
            return resp_json['error_msg']

    def get_simulation_results(self, resultType="html"):
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

    def track_simulation(self):
        if(self._trackToken == ""):
            return self._trackStatus

        url = SimulationJob.BASE_URL + 'TrackSimulation_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._trackToken
        }
        r = requests.get(url, params=payload)
        resp_json = r.json()


        if('has_more' not in resp_json):
            if('error_msg' in resp_json):
                self._trackStatus = resp_json['error_msg']
                return False
            else:
                self._trackStatus = 'Finished'
                return False

        if(resp_json['has_more'] == True):
            self._trackStatus = resp_json['doing'] + " " + str(resp_json['percent']) + "%"
            return resp_json['has_more']
        else:
            self._trackStatus = resp_json['error_msg']        
            return resp_json['has_more']

