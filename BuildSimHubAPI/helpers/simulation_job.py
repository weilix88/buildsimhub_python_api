from .energy_model import Model
import time
from .httpurllib import request_get
from .httpurllib import request_post
from .compat import is_py2


class SimulationJob:
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, user_key, model_key="", base_url=None):
        """
        Create simulation job object.

        If parameters are supplied, all parameters must be present.
        :param user_key: user api key
        :param model_key: the model key
        :param base_url: api connection url
        :type user_key: basestring
        :type model_key: basestring
        :type base_url: basestring
        """
        self._user_key = user_key
        self._model_key = model_key
        self._track_token = ""
        self._track_status = "No simulation is running or completed in this Job - " \
                             "please start simulation using create_run_model method."
        self._model_action_list = list()
        self._base_url = SimulationJob.BASE_URL

        # base_url can be reset if not None
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
        """
        future feature... TBD
        :param action:
        :return:
        """
        if action.get_num_value() > 0:
            return "Cannot process more than one value for a single simulation job. Try parametric study."
        self._model_action_list.append(action)

    def get_simulation_results(self, result_type="html"):
        """
        get a simulation result file (only use after the simulation is completed)

        :param result_type: currently available option include html, err, eso
        :return: text of the file, or error code
        :rtype: string

        """
        if self._track_token == "":
            return self._track_status

        url = self._base_url + 'GetSimulationResult_API'
        payload = {
            'user_api_key': self._user_key,
            'result_type': result_type,
            'track_token': self._track_token
        }

        r = request_post(url, params=payload, stream=True)

        if r.status_code == 200:
            return r.text
        else:
            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)

            return False

    def track_simulation(self):
        """
        track the simulation progress

        The function records the progress in self._track_status

        Example:

        status = new_sj.track_simulation()
        if status:
            print(new_sj.track_status)

        :return: True if server is still simulating the model, False otherwise
        :rtype: bool
        """
        if self._track_token == "":
            return self._track_status

        url = self._base_url + 'TrackSimulation_API'
        payload = {
            'user_api_key': self._user_key,
            'track_token': self._track_token
        }
        r = request_get(url, params=payload)
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

    def run(self, file_dir, epw_dir, unit='ip', agent=1, simulation_type='regular', track=False, request_time=5):
        """
        The function allows user to upload a model (idf, osm or gbXML) and a epw file for simulation.
        Use this method when an empty model key is supplied.

        :param file_dir: directory of the energy file (idf, osm, or gbXML)
        :param epw_dir: directory of the .epw file
        :param unit: si or ip
        :param agent: the number of agents determines how many CPU use for this simulation
        :param simulation_type: - deprecated variable - phase out soon
        :param track: true will enable tracking, also will make this function return Model object
        :param request_time: only used when tracking is true, intermittent time between each tracking request
        :type file_dir: str
        :type epw_dir: str
        :type unit: str
        :type agent: int
        :type simulation_type: str
        :type track: bool
        :type request_time: float
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model

        """
        url = self._base_url+'RunSimulationCustomize_API'
        payload = {
            'user_api_key': self._user_key,
            'simulation_type': simulation_type,
            'agents': agent,
            'unit': unit
        }

        files = dict()

        if is_py2:
            files['model'] = open(file_dir, 'r')
            files['weather_file'] = open(epw_dir, 'r')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['model'] = open(file_dir, 'r', errors='ignore')
            files['weather_file'] = open(epw_dir, 'r', errors='ignore')

        print("Submitting simulation request...")
        r = request_post(url, params=payload, files=files)
        if r.status_code == 500:
            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            self._track_status = 'Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg']
            print(self._track_status)
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
                # print(self.track_status)
                return True
        else:
            print(resp_json['error_msg'])
            return False

    def run_model_simulation(self, unit='ip', agent=1, simulation_type="regular", track=False, request_time=5):
        """
        Use this method to run a model on the BuildSimHub platform.
        Use it with create_model function

        Example:

        # key should be the model key
        new_sj = bsh.new_simulation_job("xxx-x-xxx-xx")
        new_sj.create_model("local/usr/in.idf")
        new_sj.run_model_simulation()

        :param unit: select between si and ip
        :param agent: number of CPU used for this simulation job (only accept 1, 2, and 4)
        :param simulation_type: deprecated - phase out soon
        :param track: true will enable tracking, also will make this function return Model object
        :param request_time: only used when tracking is true, intermittent time between each tracking request
        :type unit: str
        :type agent: int
        :type simulation_type: str
        :type track: bool
        :type request_time: float
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model

        """
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
        r = request_post(url, params=payload)
        if r.status_code == 500:
            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            self._track_status = 'Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg']
            print(self._track_status)
            return False
        print("Received server response")

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self.track_status)
                    time.sleep(request_time)
            print(self.track_status)
            if self.track_status == 'Simulation finished successfully':
                print(self.track_status)
                print('Completed! You can retrieve results using the key: '+self._track_token)
                # check whether there is requested data
                res = Model(self._user_key, self._track_token, self._base_url)
                return res
            else:
                # print(self.track_status)
                return True
        else:
            return resp_json['error_msg']

    def create_run_model(self, file_dir,  unit='ip', agent=1, comment="Python API", simulation_type="regular",
                         track=False, request_time=5):
        """
        this method requires supplying a project key
        Use this method to upload and run an energy model

        Example:

        # key should be the project key
        new_sj = bsh.new_simulation_job("f1fdd7ca-a327-41f1-a24b-df36d6d3dbc6")
        new_sj.create_run_model("local/usr/in.idf")

        :param file_dir:
        :param unit:
        :param agent:
        :param comment:
        :param simulation_type:
        :param track:
        :param request_time:
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model
        """
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

        files = dict()

        if is_py2:
            files['file'] = open(file_dir, 'r')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['file'] = open(file_dir, 'r', errors='ignore')

        print("Submitting simulation request...")
        r = request_post(url, params=payload, files=files)
        if r.status_code == 500:
            print(r.json())

            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            self._track_status = 'Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg']
            print(self._track_status)
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
                # print(self.track_status)
                return True
        else:
            return resp_json['error_msg']

    def create_model(self, file_dir, comment="Upload through Python API"):
        """
        Upload an energy model but no simulation
        use it with run_model_simulation() function to do simulation

        Example:

        # key should be the model key
        new_sj = bsh.new_simulation_job("xxx-x-xxx-xx")
        new_sj.create_model("local/usr/in.idf")

        :param file_dir:
        :param comment:
        :return: True, upload success or False, otherwise
        """
        url = self._base_url + 'CreateModel_API'
        payload = {
            'user_api_key': self._user_key,
            'folder_api_key': self._model_key,
            'project_api_key': self._model_key,
            'comment': comment,
            'simulation_type': '',
            'agents': 1
        }

        files = dict()

        if is_py2:
            files['file'] = open(file_dir, 'r')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['file'] = open(file_dir, 'r', errors='ignore')
        
        r = request_post(url, params=payload, files=files)
        if r.status_code == 500:
            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            self._track_status = 'Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg']
            print(self._track_status)
            return False

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
