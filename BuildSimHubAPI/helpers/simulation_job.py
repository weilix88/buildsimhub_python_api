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
                             "please start simulation using create_run_model method."
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

    def parameter_batch_modification(self, class_label, field_label, value, class_name=None, track_token=None):
        """
        This method allows user to modify an uploaded model's parameter
        Specify the class_label and field label to identify the class in the model
        if the class name is specified, then the field of class that matches the class name

        will be modified.
        :param class_label: String, class label, e.g. buildingsurface:detailed
        :param field_label:  String, field label, e.g. Zone Name
        :param value: the value that you want to wish to change to
        :param class_name: String, the name of the class: e.g. class name: ceiling_101 in field_label:name,
         under the class: buildingsurface:detail
        :param track_token: the model aip key or track token that point to the model that you want to modify
        :return: false or new model api key
        """

        if track_token is not None:
            self._track_token = track_token

        if self._track_token == "" and self._model_api_key == "":
            print("Error: Cannot modify the model if the model is not uploaded. use:"
                  " create_model() or run() or create_run_model() to upload a model")
            return False

        url = self._base_url + 'BasicModelModification_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_key,
            'class_label': class_label,
            'field_key': field_label,
            'target_value': value,
            track: self._track_token
        }

        if class_name is not None:
            payload['class_name'] = class_name

        r = request_post(url, params=payload)
        if r.status_code == 200:
            data = r.json()
            print(data['message'])
            return data['tracking']
        else:
            r_json = r.json()
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + r_json['error_msg'])
            except TypeError:
                print(r_json)
            return False

    def apply_measures(self, measure_list):
        """
        Apply energy measures on a seed model and simulate the new model.
        It should be noted that once this method is called, the simulation job class will
        update its track_token to the new model.

        :param measure_list: list of model actions
        :return: model result class

        """
        if self._track_token == "" and self._model_api_key == "":
            print("Error: Cannot modify the model if the model is not uploaded. use:"
                  " create_model() or run() or create_run_model() to upload a model")
            return False

        url = self._base_url + 'ModifyModel_API'
        track_label = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track_label = "track_token"

        payload = {
            track_label: self._track_token,
            'project_api_key': self._project_key
        }

        for i in range(len(measure_list)):
            action = measure_list[i]
            data_str = action.get_data()
            payload[action.get_api_name()] = data_str

        print('Applying measure to model: ' + self._track_token)
        r = request_post(url, params=payload)
        if r.status_code == 200:
            data = r.json()
            print(data['message'])
            return data['tracking']
        else:
            r_json = r.json()
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + r_json['error_msg'])
            except TypeError:
                print(r_json)
            return False

    def get_simulation_results(self, result_type="html", accept='file'):
        """
        This method is deprecated. It is suggested to call the same function in the result object
        returned by a successful simulation call (or use: bsh_api.helpers.Model(project_key, track_token)

        get a simulation result file (only use after the simulation is completed)
        :param result_type: currently available option include html, err, eso, eio, rdd
        :param accept:
        :return: text of the file, or error code
        :rtype: string
        """
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        url = self._base_url + 'GetSimulationResult_API'
        payload = {
            'project_api_key': self._project_key,
            'result_type': result_type,
            'accept': accept,
            track: self._track_token
        }

        r = request_post(url, params=payload, stream=True)

        if r.status_code == 200:
            return r.json()
        else:
            self._track_status = 'Code: ' + str(r.status_code)
            print(self._track_status)
            return False

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

        success = float(resp_json['success'])
        running = float(resp_json['running'])
        error = float(resp_json['error'])
        queue = float(resp_json['queue'])

        total_progress = (success + error) / (success + running + error + queue)

        message = "Total progress %d%%, success: %d, failure: %d, running: %d, queue: %d"
        self._track_status = message % (total_progress * 100, success, error, running, queue)

        if total_progress == 1:
            return False
        else:
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

    def run(self, file_dir, epw_dir, add_files=None, unit='ip', agent=1, simulation_type='regular', track=False,
            request_time=5):
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
        :param epw_dir: directory of the .epw file
        :param unit: si or ip
        :param agent: the number of agents determines how many CPU use for this simulation
        :param simulation_type: - deprecated variable - phase out soon
        :param track: true will enable tracking, also will make this function return Model object
        :param request_time: only used when tracking is true, intermittent time between each tracking request
        :param add_files: directory of a folder that contains all the additional simulation files
        :type file_dir: str
        :type epw_dir: str
        :type unit: str
        :type agent: int
        :type simulation_type: str
        :type track: bool
        :type request_time: float
        :type add_files: str
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model
        """

        url = self._base_url + 'RunSimulationCustomize_API'
        payload = {
            'simulation_type': simulation_type,
            'project_api_key': self._project_key,
            'agents': agent,
            'unit': unit
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
                        # print(self.track_status)
                        return False
                else:
                    try:
                        print(resp_json['error_msg'])
                    except:
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
                    self._track_token = resp_json['branch_key']

                    payload['branch_key'] = self._track_token

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
                        res = ParametricModel(self._track_token, self._project_key, self._base_url)

                        return res
                    else:
                        return True
                else:
                    try:
                        print(resp_json['error_msg'])
                    except:
                        print(resp_json)
                    return False
            else:
                # code check failed
                return False
        else:
            # model check failed
            print("Error: file_dir should be either a str or a list of str")
            return False

    def run_model_simulation(self, track_token=None, unit='ip', agent=1, simulation_type="regular",
                             track=False, request_time=5):
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
        :type unit: str
        :type agent: int
        :type simulation_type: str
        :type track: bool
        :type request_time: float
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
            'unit': unit
        }

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

    def create_run_model(self, file_dir,  add_files=None, unit='ip', agent=1,
                         comment="Python API", simulation_type="regular",
                         track=False, request_time=5):
        """
        this method requires supplying a project key
        Use this method to upload and run an energy model

        Example:

        # key should be the project api key
        new_sj = bsh.new_simulation_job("f1fdd7ca-a327-41f1-a24b-d3dbc6")
        new_sj.create_run_model("local/usr/in.idf", track=True) - this method will run the model

        :param file_dir: a str contains model directory or a list of str contains model directories
        :param unit:
        :param agent:
        :param comment:
        :param simulation_type:
        :param track:
        :param request_time:
        :param add_files: directory of a folder that contains all the additional simulation files
        :return: True if server accepts simulation request, False otherwise, or a Model object if tracking = True
        :rtype: bool or Model
        """
        url = self._base_url + 'CreateModel_API'
        payload = {
            'folder_api_key': self._project_key,
            'project_api_key': self._project_key,
            'comment': comment,
            'simulation_type': simulation_type,
            'agents': agent,
            'unit': unit
        }
        files = dict()

        if add_files is not None:
            # parent parent dir
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            zipf = zipfile.ZipFile(directory + '/add_folder.zip', 'w', zipfile.ZIP_DEFLATED)
            self._zip_dir(add_files, zipf)
            zipf.close()
            files['schedule_csv'] = open(directory + '/add_folder.zip', 'rb')

        if is_py2:
            files['file'] = open(file_dir, 'r')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['file'] = open(file_dir, 'r', errors='ignore')

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
                    # print(self.track_status)
                    # results are not produced
                    return False
            else:
                return resp_json['error_msg']
        else:
            # http code check error
            return False

    def create_model(self, file_dir, add_files=None, comment="Upload through Python API"):
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
        :return: True, upload success or False, otherwise
        """
        url = self._base_url + 'CreateModel_API'
        payload = {
            'project_api_key': self._project_key,
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

        if add_files is not None:
            # parent parent dir
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            zipf = zipfile.ZipFile(directory + '/add_folder.zip', 'w', zipfile.ZIP_DEFLATED)
            self._zip_dir(add_files, zipf)
            zipf.close()
            files['schedule_csv'] = open(directory + '/add_folder.zip', 'rb')

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
            except:
                print(resp_json)
            print(self._track_status)
            return False

        if resp_json['status'] == 'no_simulation':
            self._track_token = resp_json['tracking']
            print(self._track_token)
            return True
        else:
            print(resp_json['error_msg'])
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
