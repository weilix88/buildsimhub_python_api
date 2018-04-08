import requests
from .energy_model import Model
import json
import time


class SimulationJob:
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, userKey, mk, base_url=None):
        self._user_key = userKey
        self._model_key = mk
        self._track_token = ""
        self._track_status = "No simulation is running or completed in this Job - please start simulation using create_run_model method."
        self._model_action_list = list()
        self._base_url = SimulationJob.BASE_URL
        if base_url is not None:
            self._base_url = base_url

    @property
    def track_status(self):
        return self._track_status

    @property
    def track_token(self):
        return self._track_token

    @property
    def model_key(self):
        return self._model_key

    @track_token.setter
    def track_token(self, value):
        self._track_token = value

    def add_model_action(self, action):
        if action.get_num_value() > 0:
            return "Cannot process more than one value for a single simulation job. Try parametric study."
        self._model_action_list.append(action)

    def get_simulation_results(self, resultType="html"):
        if self._track_token == "":
            return self._track_status

        url = self._base_url + 'GetSimulationResult_API'
        payload = {
            'user_api_key': self._user_key,
            'result_type': resultType,
            'track_token': self._track_token
        }

        r = requests.post(url, params=payload, stream=True)

        f = ""
        if r.status_code == 200:
            f = r.text
            return f
        else:
            print('Code: ' + r.status_code)
            return False

    def track_simulation(self):
        if self._track_token == "":
            return self._track_status

        url = self._base_url + 'TrackSimulation_API'
        payload = {
            'user_api_key': self._user_key,
            'track_token': self._track_token
        }
        r = requests.get(url, params=payload)
        resp_json = r.json()

        if 'severe_error' in resp_json:
            self._track_status = resp_json['severe_error']
            return False

        if isinstance(resp_json, list):
            # parallel simulation
            sim_json = dict()
            percent = 100
            for sim_obj in resp_json:
                if 'has_more' in sim_obj:
                    if sim_obj['has_more']:
                        sim_json['has_more'] = sim_obj['has_more']
                if 'percent' in sim_obj:
                    if sim_obj['percent'] < percent:
                        sim_json['percent'] = sim_obj['percent']
                        percent = sim_obj['percent']
                        sim_json['doing'] = sim_obj['doing']
            resp_json = sim_json
        return self._track_info(resp_json)

    def run(self, file_dir, wea_dir, unit='ip', agent=1, simulation_type='regular', track=False, request_time=5):
        url = self._base_url+'RunSimulationCustomize_API'
        payload = {
            'user_api_key': self._user_key,
            'simulation_type': simulation_type,
            'agents': agent,
            'unit': unit
        }

        files = {
            'model': open(file_dir, 'rb'),
            'weather_file': open(wea_dir, 'rb')
        }

        print("Submitting simulation request...")
        r = requests.post(url, data=payload, files=files)
        if r.status_code == 500:
            print('Code: ' + r.status_code)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False
        print("Received server response")

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self.track_status)
                    time.sleep(request_time)
            if self.track_status == 'Simulation finished successfully':
                print(self.track_status)
                # check whether there is requested data
                print('Completed! You can retrieve results using the key: '+self._track_token)
                res = Model(self._user_key, self._track_token, self._base_url)
                return res
            else:
                print(self.track_status)
                return False
        else:
            print(resp_json['error_msg'])
            return False

    def run_model_simulation(self, unit='ip', agent=1, simulation_type="regular", track=False, request_time=5):
        url = self._base_url + 'RunSimulation_API'

        if self._track_token == "":
            return 'error: no model is created in this simulation job. Please create a model use create_model method.'

        payload = {
            'user_api_key': self._user_key,
            'track_token': self._track_token,
            'simulation_type': simulation_type,
            'agents': agent,
            'unit': unit
        }

        print("Submitting simulation request...")
        r = requests.post(url, data=payload)
        if r.status_code == 500:
            print('Code: ' + r.status_code)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False
        print("Received server response")

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self.track_status)
                    time.sleep(request_time)
            if self.track_status is 'Simulation finished successfully':
                print(self.track_status)
                print('Completed! You can retrieve results using the key: '+self._track_token)
                # check whether there is requested data
                res = Model(self._user_key, self._track_token, self._base_url)
                return res
            else:
                print(self.track_status)
                return False
        else:
            return resp_json['error_msg']

    def create_run_model(self, file_dir,  unit='ip', agent=1, comment="Python API", simulation_type="regular",
                         track=False, request_time=5):
        url = self._base_url + 'CreateModel_API'
        payload = {
            'user_api_key': self._user_key,
            'folder_api_key': self._model_key,
            'project_api_key': self._model_key,
            'comment': comment,
            'simulation_type': simulation_type,
            'agents': agent,
            'unit': unit
        }
        files = {
            'file': open(file_dir, 'rb')
        }

        print("Submitting simulation request...")
        r = requests.post(url, data=payload, files=files)
        if r.status_code == 500:
            print('Code: ' + r.status_code)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        print("Received server response")

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self.track_status)
                    time.sleep(request_time)
            if self.track_status is 'Simulation finished successfully':
                print(self.track_status)
                # check whether there is requested data
                print('Completed! You can retrieve results using the key: '+self._track_token)
                res = Model(self._user_key, self._track_token, self._base_url)
                return res
            else:
                print(self.track_status)
                return False
        else:
            return resp_json['error_msg']

    def create_model(self, file_dir, comment="Upload through Python API"):
        url = self._base_url + 'CreateModel_API'
        payload = {
            'user_api_key': self._user_key,
            'folder_api_key': self._model_key,
            'project_api_key': self._model_key,
            'comment': comment,
            'simulation_type': '',
            'agents': 1
        }

        files = {
            'file': open(file_dir, 'rb')
        }
        
        r = requests.post(url, data=payload, files=files)
        if r.status_code == 500:
            print('Code: ' + r.status_code)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        print(resp_json)

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            return resp_json['status']
        else:
            return resp_json['error_msg']

    def _track_info(self, resp_json):
        if 'has_more' not in resp_json:
            if 'error_msg' in resp_json:
                self._track_status = resp_json['error_msg']
                return False
            else:
                self._track_status = 'Finished'
                return False

        if resp_json['has_more']:
            self._track_status = resp_json['doing'] + " " + str(resp_json['percent']) + "%"
            return resp_json['has_more']
        else:
            if resp_json['percent'] == 100:
                self._track_status = resp_json['msg']
            # self._track_status = resp_json['error_msg']
            return resp_json['has_more']
