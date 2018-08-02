import re
import webbrowser
import json
from .httpurllib import request_get
from .httpurllib import request_post
from .httpurllib import make_url


class Model(object):
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, project_api_key, track_token, base_url=None):
        """
        Construct Model object

        Model objects use to retrieve model info and simulation results
        You can get this object by
        1. run a successful simulation using SimulationJob class: e.g.
        results = new_sj.run("in.idf","in.epw", track=True)
        if response:
            print(results.net_site_eui())

        2. get it by importing the class (you need to supply user api and either a model key or tracking token)
        results = buildsimhub.helpers.Model(project_api_key, model_api_key)
        print(results.net_site_eui())

        :param project_api_key: required
        :param track_token: required - track_token and model_api_key can be used interchangeably
        :param base_url: optional, this is only for testing purpose
        :type project_api_key: str
        :type track_token: str

        """
        self._project_api_key = project_api_key
        self._last_parameter_unit = ""
        self._track_token = track_token
        self._base_url = Model.BASE_URL
        # record all the messages in API calling
        self._log = ""

        if base_url is not None:
            self._base_url = base_url
        # if this is model api key, we will record the commit id
        test = self._track_token.split('-')
        if len(test) is not 3:
            url = self._base_url + 'GetFirstModelOfBranch_API'
            payload = {
                'project_api_key': self._project_api_key,
                'folder_api_key': self._track_token,
            }
            r = request_get(url, params=payload)
            resp_json = r.json()
            if r.status_code > 200:
                try:
                    print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
                except TypeError:
                    print(resp_json)
                    return
            if resp_json['status'] == 'success':
                self._track_token = resp_json['commit_id']
                print('find the track token...' + self._track_token)

    @property
    def project_api_key(self):
        return self._project_api_key

    @property
    def track_token(self):
        return self._track_token

    @property
    def last_parameter_unit(self):
        """The unit of data that retrieved from the latest API call"""
        return self._last_parameter_unit

    @property
    def log(self):
        return self._log

    def bldg_geo(self):
        """
        This method will open up your default browser to view the model geometry
        """
        url = self._base_url + 'IDF3DViewerSocket.html'
        track = 'model_api_key'
        test = self._track_token.split('-')
        if len(test) is 3:
            track = 'tracking'

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
        }

        r = make_url(url, payload)
        self._log = r
        webbrowser.open(r)

    def model_compare(self, target_key):
        """
        This method will open up your default browser to view the model comparison
        :param target_key: target_key is the model track_token or model_api_key
        :return:
        """
        url = self._base_url + 'ModelCompare_API'
        payload = {
            'base_model_api_key': self._track_token,
            'cmp_model_api_key': target_key
        }
        print('comparing: ' + self._track_token + ' with ' + target_key)
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
        if resp_json['status'] == 'success':
            compare_url = resp_json['url']
            webbrowser.open(compare_url)

    def model_merge(self, target_key):
        """
        Merge two models - merge the current model to the target model,
        where the target_key point at.

        :param target_key: the target model
        :return: none, a web pages shows
        """
        url = self._base_url + 'ModelMerge_API'
        payload = {
            'base_model_api_key': self._track_token,
            'cmp_model_api_key': target_key
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
        if resp_json['status'] == 'success':
            merge_url = resp_json['url']
            webbrowser.open(merge_url)

    def model_copy(self, project_api_key=''):
        """
        This function copies one model and place it in the same project
        or if the project_api_key is provided, place it to the project where
        the project_api_key point at.

        :param project_api_key: optional, project api key in str
        :return: the model id of the copied model
        """
        url = self._base_url + 'ModelCopy_API'

        payload = {
            'src_model_api_key': self._track_token
        }

        if project_api_key != '':
            payload['target_project_api_key'] = project_api_key
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
        if resp_json['status'] == 'success':
            target_proj_id = resp_json['target_project_id']
            target_branch_id = resp_json['target_branch_id']
            target_commit_id = resp_json['target_commit_id']
            track = target_proj_id + '-' + target_branch_id + '-' + target_commit_id
            print("The copied model is in project: " + target_proj_id + ", You can retrieve it with key: " +
                  track)
            return track

    def get_design_day_condition(self):
        """
        Get the design condition of the energy model from the project
        or branch (in customized project case)
        This will return a dictionary data where the key:
        'cooling': cooling design condition (99%)
        'heating': heating design condition (1%)
        'site': the site condition

        :return: design in dict data structure
        """
        url = self._base_url + 'GetDesignDayData_API'
        track = 'folder_api_key'
        test = self._track_token.split('-')
        if len(test) is 3:
            track = 'track_token'
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False
        if resp_json['status'] == 'success':
            cooling = resp_json['cooling_design_day']
            heating = resp_json['heating_design_day']
            site = resp_json['site']
            self._last_parameter_unit = ''
            design = dict()
            design['cooling'] = cooling
            design['heating'] = heating
            design['site'] = site
            return design
        else:
            return -1

    def zone_info(self, zone_name):
        """
        Get a zone's information regarding:
        lighting, people, equipment, HVAC systems
        All in SI units - IP units are not available
        All are non-normalized parameters - means lighting power is in Watts, not in watts/m2

        This method works without a simulation
        :param zone_name:
        :return:

        example output:
        {'zone_name': 'SPACE1-1', 'zone_area': '99.16000000000001', 'zone_ppl':
        '11.0', 'zone_lpd': '1702.992', 'zone_epd': '1056.0',
        'zone_heat': 'VAV Sys 1', 'zone_cool': 'VAV Sys 1', 'zone_vent': 'VAV Sys 1', 'zone_exhaust': ''}

        """
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = 'folder_api_key'
        test = self._track_token.split('-')
        if len(test) is 3:
            track = 'track_token'
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'ZoneInfo',
            'zone_name': zone_name
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False
        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            self._last_parameter_unit = ''
            return value
        else:
            return -1

    def zone_list(self):
        """
        Get the list of zones in the model,
        information include the zone name, located floor level, and whether it is conditioned or not.
        This method works without a simulation

        :return: list of dict contains each zone's information

        example output
        [{'zone_name': 'SPACE1-1', 'floor': 1, 'conditioned': 'Yes'},
        {'zone_name': 'SPACE5-1', 'floor': 1, 'conditioned': 'Yes'},
        {'zone_name': 'SPACE4-1', 'floor': 1, 'conditioned': 'Yes'},
        {'zone_name': 'SPACE3-1', 'floor': 1, 'conditioned': 'Yes'},
        {'zone_name': 'SPACE2-1', 'floor': 1, 'conditioned': 'Yes'},
        {'zone_name': 'PLENUM-1', 'floor': 2, 'conditioned': 'No'}]
        """
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = 'folder_api_key'
        test = self._track_token.split('-')
        if len(test) is 3:
            track = 'track_token'
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'ZoneList'
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['array']
            self._last_parameter_unit = ''
            return value
        else:
            return -1

    def bldg_orientation(self):
        """
        Get the building orientation.

        :return:
        """
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'Orientation'
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            self._last_parameter_unit = 'deg'

            return value
        else:
            return -1

    def num_above_ground_floor(self):
        """
        Estimate the number of floors above the ground
        :return:
        """
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'BuildingStories'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']['value']
            self._last_parameter_unit = 'floor'
            if 'total_cond_floor' in data:
                return data['total_cond_floor']
            else:
                print(data)
                return False
        else:
            return -1

    def num_total_floor(self):
        """Total floor = above ground floors + below ground floors"""
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'BuildingStories'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']['value']
            self._last_parameter_unit = 'floor'
            return data['total_floor']
        else:
            return -1

    def num_zones(self):
        """Include conditioned & unconditioned zones"""
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'TotalZoneNumber'
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            self._last_parameter_unit = 'zones'
            return data['value']
        else:
            return -1

    def num_condition_zones(self):
        """Conditioned zones only"""
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'ConditionedZoneNumber'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            self._last_parameter_unit = 'zones'
            return data['value']
        else:
            return -1

    def condition_floor_area(self, unit):
        """Total conditioned floor area"""
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'ConditionedZoneFloorArea'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = float(data['value'])
            self._last_parameter_unit = 'm2'

            if unit == 'ip':
                value = value * 10.7639
                self._last_parameter_unit = 'ft2'
            return value
        else:
            return -1

    def gross_floor_area(self, unit):
        """Total floor area"""
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'ZoneFloorArea'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = float(data['value'])
            self._last_parameter_unit = 'm2'

            if unit == 'ip':
                self._last_parameter_unit = "ft2"
                value = value * 10.7639
            return value
        else:
            return -1

    def window_wall_ratio(self):
        """Window to wall ratio"""
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': 'TotalWindowToWallRatio'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            self._last_parameter_unit = ""

            return value
        else:
            return -1

    def zone_load(self, zone_name=None):
        """
        Zone load list. If a zone_name is provided, then a detail
        zone load components will be returned

        If zone_name is not supplied, then a list of zone and their
        load info (including total heating & cooling load) will be supplied.

        Note: There will be no component load information included if zone_name is not provided

        :param zone_name:
        :return:
        """
        url = self._base_url + 'GetZoneLoadInfo_API'
        track = "folder_api_key"

        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token
        }

        if zone_name is not None:
            payload['zone_name'] = zone_name

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            zone_list = resp_json['data']
            return zone_list
        else:
            return -1

    def get_simulation_results(self, result_type="html", accept='file'):
        """
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
            'project_api_key': self._project_api_key,
            'result_type': result_type,
            'accept': accept,
            track: self._track_token
        }

        r = request_get(url, params=payload)
        if r.status_code == 200:
            if accept == 'string':
                res = json.loads(r.json())
                return res['file_name'], res['data']
            else:
                return r.json()
        else:
            js = r.json()
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + js['error_msg'])
            except TypeError:
                print(js)
                return
            return False

    def parameter_batch_modification(self, class_label, field_label, value, class_name=None):
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
        :return: false or new model api key
        """
        url = self._base_url + 'BasicModelModification_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
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
        :return: new model API key

        """
        url = self._base_url + 'ModifyModel_API'
        track_label = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track_label = "track_token"

        payload = {
            track_label: self._track_token,
            'project_api_key': self._project_api_key
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

    def download_model(self):
        """
        Help download a model from the a project
        the model will be the latest history of the model

        :return:
        """
        url = self._base_url + 'GetModel_API'

        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
        }

        r = request_get(url, params=payload)
        if r.status_code == 200:
            return r.json()
        else:
            rj = r.json()
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + rj['error_msg'])
            except TypeError:
                print(rj)
            return False

    def hourly_data(self, data=None):

        variable_list_request = False

        if data is None:
            variable_list_request = True

        url = self._base_url + 'GetHourlyVariableFromEso_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
        }

        if not variable_list_request:
            payload['variable'] = data

        r = request_get(url, params=payload)
        if r.status_code == 200:
            data_array = r.json()['data']

            if variable_list_request:
                variable_list = data_array['variableList']
            else:
                variable_list = data_array['value'][data]

            return variable_list
        else:
            rj = r.json()
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + rj['error_msg'])
            except TypeError:
                print(rj)
            return False

    def html_table(self, report, table, report_for='EntireFacility'):
        """
        get an HTML table for plot
        :param report: report name e.g. Annual Building Utility Performance Summary
        :param table: table name e.g. End Uses
        :param report_for: typically it is EntireFacility, but with some exceptions
        :return:
        """
        url = self._base_url + 'GetTableFromHTML_API'

        r = re.sub('\W', '', report)
        t = re.sub('\W', '', table)
        rf = re.sub('\W', '', report_for)

        table_id = r + ":" + rf + ":" + t

        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'table_name': table_id
        }

        r = request_get(url, params=payload)
        if r.status_code == 200:
            return r.json()
        else:
            rj = r.json()
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + rj['error_msg'])
            except TypeError:
                print(rj)
            return False

    def monthly_electricity(self):
        return self.__monthly_call_api('ElectricityMonthly')

    def monthly_hvac_air_system_load(self, air_system=None):
        return self.__monthly_call_api('HVACAirSystemLoadsMonthly', air_system)

    def monthly_hvac_system_energy(self):
        return self.__monthly_call_api('HVACSystemEnergyMonthly')

    def monthly_natural_gas(self):
        return self.__monthly_call_api('NaturalGasMonthly')

    def monthly_occupant_comfort_zone(self, zone=None):
        return self.__monthly_call_api('OccupantComfortZoneMonthly', zone)

    def monthly_outdoor_air_zone(self, zone=None):
        return self.__monthly_call_api('OutdoorAirZoneMonthly', zone)

    def monthly_setpoint_not_met_zone(self, zone=None):
        return self.__monthly_call_api('SetpointNotMetZoneMonthly', zone)

    # Below are the methods use for retrieving results
    def net_site_eui(self):
        return self.__call_api('NetSiteEUI')

    def total_site_eui(self):
        return self.__call_api('TotalSiteEUI')

    def not_met_hour_cooling(self):
        return self.__call_api('NotMetHoursCooling')

    def not_met_hour_heating(self):
        return self.__call_api('NotMetHoursHeating')

    def not_met_hour_total(self):
        return self.__call_api('NotMetHoursTotal')

    def total_end_use_electricity(self):
        return self.__call_api('TotalEndUseElectricity')

    def total_end_use_naturalgas(self):
        return self.__call_api('TotalEndUseNaturalGas')

    def cooling_electricity(self):
        return self.__call_api('CoolingElectricity')

    def cooling_naturalgas(self):
        return self.__call_api('CoolingNaturalGas')

    def domestic_hotwater_electricity(self):
        return self.__call_api('DomesticHotWaterElectricity')

    def domestic_hotwater_naturalgas(self):
        return self.__call_api('DomesticHotWaterNaturalGas')

    def exterior_equipment_electricity(self):
        return self.__call_api('ExteriorEquipmentElectricity')

    def exterior_equipment_naturalgas(self):
        return self.__call_api('ExteriorEquipmentElectricity')

    def exterior_lighting_electricity(self):
        return self.__call_api('ExteriorLightingElectricity')

    def exterior_lighting_naturalgas(self):
        return self.__call_api('ExteriorLightingNaturalGas')

    def fan_electricity(self):
        return self.__call_api('FansElectricity')

    def fan_naturalgas(self):
        return self.__call_api('FansNaturalGas')

    def heating_electricity(self):
        return self.__call_api('HeatingElectricity')

    def heating_naturalgas(self):
        return self.__call_api('HeatingNaturalGas')

    def heat_rejection_electricity(self):
        return self.__call_api('HeatRejectionElectricity')

    def heat_rejection_naturalgas(self):
        return self.__call_api('HeatRejectionNaturalGas')

    def interior_equipment_electricity(self):
        return self.__call_api('InteriorEquipmentElectricity')

    def interior_equipment_naturalgas(self):
        return self.__call_api('InteriorEquipmentNaturalGas')

    def interior_lighting_electricity(self):
        return self.__call_api('InteriorLightingElectricity')

    def interior_lighting_naturalgas(self):
        return self.__call_api('InteriorLightingNaturalGas')

    def pumps_electricity(self):
        return self.__call_api('PumpsElectricity')

    def pumps_naturalgas(self):
        return self.__call_api('PumpsNaturalGas')

    def bldg_lpd(self):
        return self.__call_api('BuildingLPD')

    def bldg_epd(self):
        return self.__call_api('BuildingEPD')

    def bldg_ppl(self):
        return self.__call_api('BuildingPPL')

    def wall_rvalue(self):
        return self.__call_api('WallRValue')

    def roof_rvalue(self):
        return self.__call_api('RoofRValue')

    def window_uvalue(self):
        return self.__call_api('WindowUValue')

    def window_shgc(self):
        return self.__call_api('WindowSHGC')

    def roof_absorption(self):
        return self.__call_api('RoofAbsorption')

    def bldg_infiltration(self):
        return self.__call_api('Infiltration')

    def bldg_water_heater_efficiency(self):
        return self.__call_api('WaterHeaterEfficiency')

    def bldg_dx_cooling_efficiency(self):
        return self.__call_api('DXCoolingCoilEfficiency')

    def bldg_chiller_efficiency(self):
        return self.__call_api('ChillerEfficiency')

    def bldg_electric_boiler_efficiency(self):
        return self.__call_api('ElectricBoilerEfficiency')

    def bldg_fuel_boiler_efficiency(self):
        return self.__call_api('FuelBoilerEfficiency')

    def bldg_dx_heating_efficiency(self):
        return self.__call_api('ElectricHeatingDXCoils')

    def __monthly_call_api(self, request_data, request_component=None):
        url = self._base_url + 'GetBuildingMonthlyResults_API'
        track = 'folder_api_key'

        test = self._track_token.split("-")
        if len(test) is 3:
            track = 'track_token'

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': request_data
        }

        if request_component is not None:
            payload['request_for'] = request_component

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False
        if resp_json['status'] == 'success':
            data = resp_json['data']
            value_type = data['type']
            collections = data['collection']

            if value_type == 'Numeric':
                value = data['value']
                if 'unit' in data:
                    self._last_parameter_unit = data['unit']
                return value
            elif value_type == 'JsonObject':
                if collections == 'true':
                    value = data['array']
                    return value
                else:
                    value = data['value']
                    return value
        else:
            return -1

    def __call_api(self, request_data):
        url = self._base_url + 'GetBuildingSimulationResults_API'
        track = "folder_api_key"

        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_api_key,
            track: self._track_token,
            'request_data': request_data
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            try:
                print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            except TypeError:
                print(resp_json)
                return
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']

            value_type = data['type']
            collections = data['collection']

            if value_type == 'Numeric':
                value = data['value']
                if 'unit' in data:
                    self._last_parameter_unit = data['unit']
                return value
            elif value_type == 'JsonObject':
                if collections == 'true':
                    value = data['array']
                    return value
                else:
                    value = data['value']
                    return value
        else:
            return -1
