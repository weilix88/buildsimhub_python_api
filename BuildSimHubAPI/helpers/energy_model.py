import webbrowser
from .httpurllib import request_get


class Model:
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, user_key, model_key, base_url=None):
        """
        Construct Model object

        Model objects use to retrieve model info and simulation results
        You can get this object by
        1. run a successful simulation using SimulationJob class: e.g.
        results = new_sj.run("in.idf","in.epw", track=True)
        if response:
            print(results.net_site_eui())

        2. get from BuildSim API client with a simulation job
        results = bsh.get_simulation_results(new_sj)
        print(results.net_site_eui())

        3. get it by importing the class (you need to supply user api and either a model key or tracking token)
        results = buildsimhub.helpers.Model(user_api, model_key)
        print(results.net_site_eui())

        :param user_key:
        :param model_key:
        :param base_url: optional, this is only for testing purpose
        :type user_key: str
        :type model_key: str

        """
        self._user_key = user_key
        self._last_parameter_unit = ""
        self._model_key = model_key
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
        test = self._model_key.split('-')
        if len(test) is 3:
            track = 'tracking'

        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
        }

        r = request_get(url, params=payload)
        self._log = r.url
        webbrowser.open(r.url)

    def bldg_orientation(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'Orientation'
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'BuildingStories'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'BuildingStories'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'TotalZoneNumber'
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code)+ ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'ConditionedZoneNumber'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'ConditionedZoneFloorArea'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code)+ ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'ZoneFloorArea'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code)+ ' message: ' + resp_json['error_msg'])
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
        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': 'TotalWindowToWallRatio'
        }
        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
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

        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._user_key,
            track: self._model_key
        }

        if zone_name is not None:
            payload['zone_name'] = zone_name

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code)+ ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            zone_list = resp_json['data']
            return zone_list
        else:
            return -1

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
        return self.__call_api('FanElectricity')

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
        return self.__call_api('InteiorEquipmentElectricity')

    def interior_equipment_naturalgas(self):
        return self.__call_api('InteirorEquipmentNaturalGas')

    def interior_lighting_electricity(self):
        return self.__call_api('InteriorLightingElectricity')

    def interior_lighting_naturalgas(self):
        return self.__call_api('InteriorLightingNaturalGas')

    def pumps_electricity(self):
        return self.__call_api('PumpsElectricity')

    def pumps_naturalgas(self):
        return self.__call_api('PumpsNaturalGas')

    def __call_api(self, request_data):
        url = self._base_url + 'GetBuildingSimulationResults_API'
        track = "folder_api_key"

        test = self._model_key.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
            'request_data': request_data
        }

        r = request_get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + str(r.status_code) + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            if 'unit' in data:
                self._last_parameter_unit = data['unit']
            return value
        else:
            return -1
