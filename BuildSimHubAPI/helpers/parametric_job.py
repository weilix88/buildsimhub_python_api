import time
from .httpurllib import request_get
from .httpurllib import request_post
from .parametric_model import ParametricModel
from .compat import is_py2


class ParametricJob(object):
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, user_key, model_key, base_url=None):
        """
        Construct a parametric job

        Specify EEM and do parametrics

        :param user_key:
        :param model_key:
        :param base_url: optional - use for testing only
        :type user_key: str
        :type model_key: str
        :type base_url: str
        """
        self._user_key = user_key
        self._model_key = model_key
        self._track_token = ""
        self._track_status = ""
        # list of data
        self._model_action_list = list()
        self._base_url = ParametricJob.BASE_URL
        if base_url is not None:
            self._base_url = base_url

    @property
    def track_token(self):
        return self._track_token

    def get_status(self):
        """Get the tracking status"""
        return self._track_status

    def set_track_token(self, track_token):
        self._track_token = track_token
        return True

    def add_model_measures(self, measures):
        """
        Add measures
        :param measures: list of measures
        :type measures: list of ModelAction
        """
        for measure in measures:
            self._model_action_list.append(measure)

    def add_model_measure(self, measure):
        """
        Add a measure
        :param measure: a measure
        :type measure: ModelAction
        """
        self._model_action_list.append(measure)

    def num_total_combination(self):
        """Number of combinations based on the number of EEM & number of options for each EEM"""
        num_total = 0
        for i in range(len(self._model_action_list)):
            if num_total == 0:
                num_total = self._model_action_list[i].get_num_value()
            else:
                num_total = num_total * self._model_action_list[i].get_num_value()
        return num_total

    def submit_parametric_study_local(self, file_dir, unit='ip', simulation_type="parametric",
                                      track=False, request_time=5):
        """
        Submit an energy model from local as the seed model to a project for this parametric study
        Example:
            project_key = "xxx"
            file_dir = "in.idf"
            new_sj = buildsimhub.new_parametric_job(project_key)
            new_sj.submit_parametric_study_local(file_dir, track=True)

        :param file_dir:
        :param unit:
        :param simulation_type: deprecated
        :param track:
        :param request_time:
        :type file_dir: str
        :type unit: str (ip or si)
        :type simulation_type: str
        :type track: bool
        :type request_time: float
        :return: True success, False otherwise
        """
        # file_dir indicates the seed model
        url = self._base_url + 'ParametricSettingUploadModel_API'
        payload = {
            'user_api_key': self._user_key,
            'project_api_key': self._model_key,
            'simulation_type': simulation_type,
            'agents': 1,
            'unit': unit
        }

        for i in range(len(self._model_action_list)):
            measure = self._model_action_list[i]
            payload[measure.get_api_name()] = measure.get_data_string()

        files = dict()

        if is_py2:
            files['model'] = open(file_dir, 'r')
        else:
            # py3 cannot decode incompatible utf-8 string
            files['model'] = open(file_dir, 'r', errors='ignore')

        print('Submitting parametric simulation job request...')
        r = request_post(url, params=payload, files=files)
        if r.status_code == 500:
            print('Code: ' + str(r.status_code))
            return False
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            return False
        print('Received server response')

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self._track_status)
                    time.sleep(request_time)
                print(self._track_status)
                print('Completed! You can retrieve results using the key: ' + self._track_token)
                res = ParametricModel(self._user_key, self._track_token, self._base_url)
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
    #            'user_api_key': self._user_key,
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
    #            self._track_token = resp_json['tracking']
    #            return resp_json['status']
    #        else:
    #            return resp_json['error_msg']

    # for this method, it allows user to identify one seed model in a project.
    # This allows the parametric study performed under a project with a fixed weather file,
    def submit_parametric_study(self, unit='ip', simulation_type='parametric', track=False, request_time=5):
        """
        Select a model in the project as the seed model and do parametric study

        Example:
            model_key = "xx"

            new_pj = bsh.new_parametric_job(model_key)
            new_pj.submit_parametric_study(track=True)

        :param unit:
        :param simulation_type: deprecated
        :param track:
        :param request_time:
        :type unit: str
        :type simulation_type: str
        :type track: bool
        :type request_time: float
        :return: True if success, False otherwise
        """
        url = self._base_url + 'ParametricSettingCopyModel_API'
        payload = {
            'user_api_key': self._user_key,
            'model_api_key': self._model_key,
            'simulation_type': simulation_type,
            'agents': 1,
            'unit': unit
        }

        for i in range(len(self._model_action_list)):
            action = self._model_action_list[i]
            payload[action.get_api_name()] = action.get_data_string()

        # return payload
        print('Submitting parametric simulation job request...')
        r = request_post(url, params=payload)
        if r.status_code == 500:
            print(r.json())
            print('Code: ' + str(r.status_code))
            return False
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            return False
        print('Received server response')

        if resp_json['status'] == 'success':
            self._track_token = resp_json['tracking']
            if track:
                while self.track_simulation():
                    print(self._track_status)
                    time.sleep(request_time)
                print(self._track_status)
                print('Completed! You can retrieve results using the key: ' + self._track_token)
                res = ParametricModel(self._user_key, self._track_token, self._base_url)
                return res
            else:
                return True
        else:
            print(resp_json['error_msg'])
            return False

    def track_simulation(self):
        if self._track_token == "":
            return self._track_status

        url = self._base_url + 'ParametricTracking_API'
        payload = {
            'user_api_key': self._user_key,
            'folder_api_key': self._track_token
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
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
