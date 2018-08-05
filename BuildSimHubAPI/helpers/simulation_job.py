from .energy_model import Model
import time
from .httpurllib import request_get
from .httpurllib import request_post
from .compat import is_py2
from .parametric_model import ParametricModel
import os
import zipfile


class SimulationJob(object):
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, project_key, base_url=None):
        """
        Create simulation job object.

        If parameters are supplied, all parameters must be present.
        :param project_key: the project key, required
        :param base_url: api connection url
        :type project_key: basestring
        :type base_url: basestring
        """
        self._project_key = project_key
        self._track_token = ""
        self._track_status = "No simulation is running or completed in this Job - " \
                             "please start simulation using run method."
        self._model_action_list = list()
        self._base_url = SimulationJob.BASE_URL
        self._model_api_key = ""

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
    def model_api_key(self):
        return self._model_api_key

    @property
    def project_key(self):
        return self._project_key

    @track_token.setter
    def track_token(self, value):
        self._track_token = value

    def track_batch_simulation(self):
        if self._track_token == "":
            return self._track_status

        url = self._base_url + 'ParametricTracking_API'
        payload = {
            'folder_api_key': self._track_token,
            'project_api_key': self._project_key
        }

        try:
            r = request_get(url, params=payload)
            resp_json = r.json()
        except ConnectionResetError:
            return "Reconnecting to server..."

        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
            return False

        if 'error_msg' in resp_json:
            self._track_status = resp_json['error_msg']
            return False

        if 'success' in resp_json:

            success = float(resp_json['success'])
            running = float(resp_json['running'])
            error = float(resp_json['error'])
            queue = float(resp_json['queue'])

            divider = success + running + error + queue
            if divider == 0:
                total_progress = 1
            else:
                total_progress = (success + error) / divider

            message = "Total progress %d%%, success: %d, failure: %d, running: %d, queue: %d"
            self._track_status = message % (total_progress * 100, success, error, running, queue)

            if total_progress == 1:
                return False
            else:
                return True
        else:
            print(resp_json['message'])
            return True

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
            'track_token': self._track_token,
            'project_api_key': self._project_key
        }

        try:
            r = request_get(url, params=payload)
            resp_json = r.json()
        except ConnectionResetError:
            return "Reconnecting to server..."

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

    def run(self, file_dir, epw_dir=None, add_files=None, unit='ip', design_condition='no', agent=1,
            comment="Python API", track=False, request_time=5):
        """
        The function allows user to upload a model (idf, osm or gbXML) and a epw file for simulation.
        Use this method when an empty model key is supplied. It should be noted, although a project api key is required
        for this method, however, this method is only use the CPUs from the linked project api key for simulation, but
        the upload model does not associate with the project.
        For example: user use a project api key a-b-c for simulation. This method will use one of the CPUs
        in the project a-b-c. However, the submitted model does not belong to the project a-b-c.
        If user wish to retrieve the model information. user can either use the python library:

        bsh.model_results(project_api_key, track_token)

        or go to the simulation dashboard on the web UI to manually retrieve the model results.

        :param file_dir: directory of the energy file (idf, osm, or gbXML) or list of directories
        :param epw_dir: directory of the .epw file, only customized project supports this function
        :param unit: si or ip
        :param agent: the number of agents determines how many CPU use for this simulation
        :param comment: the name of the uploaded model
        :param track: true will enable tracking, also will make this function return Model object
        :param request_time: only used when tracking is true, intermittent time between each tracking request
        :param add_files: directory of a folder that contains all the additional simulation files
        :param design_condition: default is no, if yes, the function will attempt to modify the design day condition
                using ASHRAE design condition 2013 data based on the closest weather station / lat and lon.
        :type file_dir: str
        :type epw_dir: str
        :type unit: str
        :type agent: int
        :type track: bool
        :type request_time: float
        :type add_files: str
        :type design_condition: yes or no
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model
        """

        url = self._base_url + 'CreateModel_API'
        payload = {
            'project_api_key': self._project_key,
            'agents': agent,
            'comment': comment,
            'design_cond': design_condition,
            'unit': unit,
            'do_load_simulation': 'no'
        }

        if type(file_dir) is str:

            files = self._decode_model_and_epw(file_dir, epw_dir)

            if add_files is not None:
                # parent parent dir
                directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                zipf = zipfile.ZipFile(directory+'/add_folder.zip', 'w', zipfile.ZIP_DEFLATED)
                self._zip_dir(add_files, zipf)
                zipf.close()
                files['schedule_csv'] = open(directory+'/add_folder.zip', 'rb')
            print("Submitting simulation request...")
            r = request_post(url, params=payload, files=files)
            if self._http_code_check(r):
                resp_json = r.json()
                if resp_json['status'] == 'success':
                    self._track_token = resp_json['tracking']
                    self._model_api_key = resp_json['model_api_key']
                    if track:
                        while self.track_simulation():
                            print(self.track_status)
                            time.sleep(request_time)
                    if self.track_status == 'Simulation finished successfully':
                        print(self.track_status)
                        # check whether there is requested data
                        print('Completed! You can retrieve results using the key: '+self._track_token)
                        res = Model(self._project_key, self._track_token, self._base_url)
                        return res
                    else:
                        print(self.track_status)
                        return False
                else:
                    try:
                        print(resp_json['error_msg'])
                    except KeyError:
                        print(resp_json)
                    return False
            else:
                return False
        elif type(file_dir) is list:
            if len(file_dir) == 0:
                print("Model directory list should not be empty")
                return False
            print("Submitting the model number: 1")
            files = self._decode_model_and_epw(file_dir[0], epw_dir)

            if add_files is not None:
                # parent parent dir
                directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                zipf = zipfile.ZipFile(directory+'/add_folder.zip', 'w', zipfile.ZIP_DEFLATED)
                self._zip_dir(add_files, zipf)
                zipf.close()
                files['schedule_csv'] = open(directory+'/add_folder.zip', 'rb')

            r = request_post(url, params=payload, files=files)
            if self._http_code_check(r):
                resp_json = r.json()
                if resp_json['status'] == 'success':
                    # in this case, we are getting the branch key / model key
                    self._track_token = resp_json['model_api_key']
                    self._model_api_key = resp_json['model_api_key']
                    payload['model_api_key'] = self._track_token
                    for i in range(1, len(file_dir)):
                        time.sleep(5)
                        print("Submitting the model number: " + str(i + 1))
                        files = self._decode_model_and_epw(file_dir[i], None)
                        r = request_post(url, params=payload, files=files)
                        if self._http_code_check(r):
                            resp_json = r.json()
                            if resp_json['status'] == 'error':
                                print(resp_json['error_msg'])
                                return False
                        else:
                            return False
                    if track:
                        while self.track_batch_simulation():
                            print(self._track_status)
                            time.sleep(request_time)
                        print(self._track_status)
                        print('Completed! You can retrieve results using the key: '+self._track_token)
                        res = ParametricModel(self._project_key, self._track_token, self._base_url)

                        return res
                    else:
                        return True
                else:
                    try:
                        print(resp_json['error_msg'])
                    except KeyError:
                        print(resp_json)
                    return False
            else:
                # code check failed
                return False
        else:
            # model check failed
            print("Error: file_dir should be either a str or a list of str")
            return False

    def run_model_simulation(self, track_token=None, unit='ip', design_condition='no', agent=1,
                             simulation_type="regular", track=False, request_time=5):
        """
        Use this method to run an un-simulated model under a project.

        Example:

        # key should be the model key
        //this example firstly uploads a model to the project
        //and then run the model under the project
        new_sj = bsh.new_simulation_job("xxx-x-xxx-xx")
        new_sj.create_model("local/usr/in.idf")
        new_sj.run_model_simulation()

        or:
        //this example run the xxx-xxx-xxx model under the project:
        abc-def-ghijk - the xxx-xxx-xxx model needs to be in the project and has not been simulated

        new_sj = bsh.new_simulation_job("abc-def-ghijk")
        new_sj.run_model_simulation("xxx-xxx-xxx")

        :param unit: select between si and ip
        :param track_token: If use for an exist model on the web platform
        :param agent: number of CPU used for this simulation job (only accept 1, 2, and 4)
        :param simulation_type: deprecated - phase out soon
        :param track: true will enable tracking, also will make this function return Model object
        :param request_time: only used when tracking is true, intermittent time between each tracking request
        :param design_condition: default is no. If yes, BuildSim cloud will attempt to update the design day condition
            with the project specified design day condition.
            The condition is extracted from ASHRAE design condition 2013
        :type unit: str
        :type agent: int
        :type simulation_type: str
        :type track: bool
        :type request_time: float
        :type design_condition: no or yes
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model

        """
        url = self._base_url + 'RunSimulation_API'

        if track_token is not None:
            self._track_token = track_token

        if self._track_token == "":
            return 'error: no model is created in this simulation job. ' \
                       'Please create a model use create_model method.'

        payload = {
            'project_api_key': self._project_key,
            'track_token': self._track_token,
            'simulation_type': simulation_type,
            'agents': agent,
            'design_cond': design_condition,
            'unit': unit,
        }

        if simulation_type == 'regular':
            payload['do_load_simulation'] = 'no'
        else:
            payload['do_load_simulation'] = 'yes'

        print("Submitting simulation request...")
        r = request_post(url, params=payload)
        if self._http_code_check(r):
            resp_json = r.json()
            if resp_json['status'] == 'success':
                self._track_token = resp_json['tracking']
                if track:
                    while self.track_simulation():
                        print(self.track_status)
                        time.sleep(request_time)
                print(self.track_status)
                if self.track_status == 'Simulation finished successfully':
                    print('Completed! You can retrieve results using the key: ' + self._track_token)
                    # check whether there is requested data
                    res = Model(self._project_key, self._track_token, self._base_url)
                    return res
                else:
                    # print(self.track_status)
                    return True
            else:
                return resp_json['error_msg']
        else:
            # http code check error
            return False

    def create_run_model(self, file_dir, epw_dir=None, add_files=None, unit='ip', design_condition='no', agent=1,
                        comment="Python API", track=False, request_time=5):
        """
        deprecated - works the same as the run function now.

        :param file_dir: directory of the energy file (idf, osm, or gbXML) or list of directories
        :param epw_dir: directory of the .epw file, only customized project supports this function
        :param unit: si or ip
        :param agent: the number of agents determines how many CPU use for this simulation
        :param comment: the name of the uploaded model
        :param track: true will enable tracking, also will make this function return Model object
        :param request_time: only used when tracking is true, intermittent time between each tracking request
        :param add_files: directory of a folder that contains all the additional simulation files
        :param design_condition: default is no, if yes, the function will attempt to modify the design day condition
                using ASHRAE design condition 2013 data based on the closest weather station / lat and lon.
        :type file_dir: str
        :type epw_dir: str
        :type unit: str
        :type agent: int
        :type track: bool
        :type request_time: float
        :type add_files: str
        :type design_condition: yes or no
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model
        """
        return self.run(file_dir, epw_dir, add_files, unit, design_condition, agent,
                        comment, track, request_time)

    def create_model(self, file_dir, epw_dir=None, add_files=None, comment="Upload through Python API"):
        """
        Upload an energy model but no simulation
        use it with run_model_simulation() function to do simulation

        Example:

        # key should be the model key
        new_sj = bsh.new_simulation_job("xxx-x-xxx-xx")
        new_sj.create_model("local/usr/in.idf")

        :param file_dir:
        :param comment:
        :param add_files: directory of a folder that contains all the additional simulation files
        :param epw_dir: weather file -optional only customized project supports this function
        :return: True, upload success or False, otherwise
        """
        url = self._base_url + 'CreateModel_API'
        payload = {
            'project_api_key': self._project_key,
            'comment': comment,
            'do_load_simulation': 'no',
            'agents': ''
        }

        files = dict()

        if is_py2:
            files['model'] = open(file_dir, 'r')
            if epw_dir is not None:
                files['weather_file'] = open(epw_dir, 'r')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['model'] = open(file_dir, 'r', errors='ignore')
            if epw_dir is not None:
                files['weather_file'] = open(epw_dir, 'r', errors='ignore')

        if add_files is not None:
            # parent parent dir
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            zipf = zipfile.ZipFile(directory + '/add_folder.zip', 'w', zipfile.ZIP_DEFLATED)
            self._zip_dir(add_files, zipf)
            zipf.close()
            files['schedule_csv'] = open(directory + '/add_folder.zip', 'rb')

        print('submitting model to the server...')
        r = request_post(url, params=payload, files=files)
        if r.status_code == 500:
            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)
            return False
        resp_json = r.json()
        if r.status_code > 200:
            try:
                self._track_status = 'Code: ' + str(r.status_code) + \
                    ' message: ' + resp_json['error_msg']
            except (KeyError, TypeError):
                print(self._track_status)
            return False

        if resp_json['status'] == 'no_simulation':
            self._track_token = resp_json['tracking']
            self._model_api_key = resp_json['model_api_key']
            print(self._track_token)
            return Model(self.project_key, self._track_token, self._base_url)
        else:
            if 'error_msg' in resp_json:
                print(resp_json['error_msg'])
            else:
                print(resp_json)
            return False

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

    @staticmethod
    def _decode_model_and_epw(model, epw):
        files = dict()
        if is_py2:
            files['model'] = open(model, 'rb')
            if epw is not None:
                files['weather_file'] = open(epw, 'rb')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['model'] = open(model, 'rb')
            if epw is not None:
                files['weather_file'] = open(epw, 'rb')
        return files

    @staticmethod
    def _zip_dir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), arcname=file)

    def _http_code_check(self, resp):
        if resp.status_code == 500:
            self._track_status = 'Code: ' + str(resp.status_code)
            print(self._track_status)
            return False
        resp_json = resp.json()
        if resp.status_code > 200:
            try:
                self._track_status = 'Code: ' + \
                    str(resp.status_code) + ' message: ' + resp_json['error_msg']
            except TypeError:
                print(resp_json)
            print(self._track_status)
            return False
        # None of those code, then it should be 200
        print("Received server response")
        return True
