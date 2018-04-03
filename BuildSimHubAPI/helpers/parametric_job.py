import requests
import json
import time
from .parametric_model import ParametricModel


class ParametricJob():
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, userKey, mk, base_url=None):
        self._userKey = userKey
        self._modelKey = mk
        self._trackToken = ""
        self._trackStatus = ""
        # list of data
        self._model_action_list = list()
        self._base_url = ParametricJob.BASE_URL
        if base_url is not None:
            self._base_url = base_url

    @property
    def trackToken(self):
        return self._trackToken

    def get_status(self):
        return self._trackStatus

    def add_model_measures(self, measures):
        for measure in measures:
            self._model_action_list.append(measure)

    def add_model_measure(self, action):
        self._model_action_list.append(action)

    def num_total_combination(self):
        num_total = 0
        for i in range(len(self._model_action_list)):
            if num_total == 0:
                num_total = self._model_action_list[i].get_num_value()
            else:
                num_total = num_total * self._model_action_list[i].get_num_value()
        return num_total

    def submit_parametric_study_local(self, file_dir, unit='ip', simulation_type="parametric", track=False, request_time=5):
        # file_dir indicates the seed model
        url = self._base_url + 'ParametricSettingUploadModel_API'
        payload = {
            'user_api_key': self._userKey,
            'project_api_key': self._modelKey,
            'simulation_type': simulation_type,
            'agents': 1,
            'unit': unit
        }

        for i in range(len(self._model_action_list)):
            measure = self._model_action_list[i]
            payload[measure.get_api_name()] = measure.get_data_string()

        files = {
            'model': open(file_dir, 'rb')
        }

        print('Submitting parametric simulation job request...')
        r = requests.post(url, data=payload, files=files)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False
        print('Received server response')

        if resp_json['status'] == 'success':
            self._trackToken = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self._trackStatus)
                    time.sleep(request_time)
                print(self._trackStatus)
                print('Completed! You can retrieve results using the key: '+self._trackToken)
                res = ParametricModel(self._userKey, self._trackToken, self._base_url)
                return res
            else:
                return True
        else:
            print(resp_json['error_msg'])
            return False
    # For this method, it allows user to upload energy model from local machine, along with the weather file
    # this will creates a new project each time and run the parametric simulation.
    #    def submit_parametric_study_local(self, file_dir, wea_dir, simulationType ="parametric"):
    # file_dir indicates the seed model
    #        url = ParametricJob.BASE_URL + 'CreateModel_API'
    #        payload = {
    #            'user_api_key': self._userKey,
    #            'simulation_type': simulationType,
    #            'agents':1
    #        }

    #        for i in range(len(self._model_action_list)):
    #            action = self._model_action_list[i]
    #            payload[action.get_api_name()] = action.get_datalist()

    #        files = {
    #            'file': open(file_dir, 'rb')
    #        }

    #        r = requests.post(url, data=payload, files= files)

    #        resp_json = r.json()

    #        if(resp_json['status'] == 'success'):
    #            self._trackToken = resp_json['tracking']
    #            return resp_json['status']
    #        else:
    #            return resp_json['error_msg']

    # for this method, it allows user to identify one seed model in a project.
    # This allows the parametric study performed under a project with a fixed weather file,
    def submit_parametric_study(self, unit='ip', simulation_type='parametric', track=False, request_time=5):

        url = self._base_url + 'ParametricSettingCopyModel_API'
        payload = {
            'user_api_key': self._userKey,
            'model_api_key': self._modelKey,
            'simulation_type': simulation_type,
            'agents': 1,
            'unit': unit
        }

        for i in range(len(self._model_action_list)):
            action = self._model_action_list[i]
            payload[action.get_api_name()] = action.get_data_string()

        # return payload
        print('Submitting parametric simulation job request...')
        r = requests.post(url, data=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False
        print('Received server response')

        if resp_json['status'] == 'success':
            self._trackToken = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self._trackStatus)
                    time.sleep(request_time)
                print(self._trackStatus)
                print('Completed! You can retrieve results using the key: '+self._trackToken)
                res = ParametricModel(self._userKey, self._trackToken, self._base_url)
                return res
            else:
                return True
        else:
            print(resp_json['error_msg'])
            return False

    def track_simulation(self):
        if self._trackToken == "":
            return self._trackStatus

        url = self._base_url + 'ParametricTracking_API'
        payload = {
            'user_api_key': self._userKey,
            'folder_api_key': self._trackToken
        }

        r = requests.get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if 'error_msg' in resp_json:
            self._trackStatus = resp_json['error_msg']
            return False

        success = float(resp_json['success'])
        running = float(resp_json['running'])
        error = float(resp_json['error'])
        queue = float(resp_json['queue'])

        totalProgress = (success + error) / (success + running + error + queue)

        message = "Total progress %d%%, success: %d, failure: %d, running: %d, queue: %d"
        self._trackStatus = message % (totalProgress * 100, success, error, running, queue)

        if totalProgress == 1:
            return False
        else:
            return True
