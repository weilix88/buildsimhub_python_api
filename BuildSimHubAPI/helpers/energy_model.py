import re
import webbrowser
import json
from .httpurllib import request_get
from .httpurllib import make_url


class Model(object):
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, project_key, track_token, base_url=None):
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

        :param project_key: required
        :param track_token: required
        :param base_url: optional, this is only for testing purpose
        :type project_key: str
        :type track_token: str

        """
        self._project_key = project_key
        self._last_parameter_unit = ""
        self._track_token = track_token
        self._base_url = Model.BASE_URL
        # record all the messages in API calling
        self._log = ""

        if base_url is not None:
            self._base_url = base_url

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
            'project_api_key': self._project_key,
            track: self._track_token,
        }

        r = make_url(url, payload)
        self._log = r
        webbrowser.open(r)

    def bldg_orientation(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            data = resp_json['data']
            self._last_parameter_unit = 'floor'
            return data['total_cond_floor']
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
            'project_api_key': self._project_key,
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
            data = resp_json['data']
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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
            'project_api_key': self._project_key,
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

    def __call_api(self, request_data):
        url = self._base_url + 'GetBuildingSimulationResults_API'
        track = "folder_api_key"

        test = self._track_token.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'project_api_key': self._project_key,
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
            value = data['value']
            if 'unit' in data:
                self._last_parameter_unit = data['unit']
            return value
        else:
            return -1
