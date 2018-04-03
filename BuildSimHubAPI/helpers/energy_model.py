import requests
import webbrowser
# This is a class that contains all the model information for user
# to read


# potentially in the future, to write

class Model:

    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, user_key, model_key, base_url=None):
        self._userKey = user_key
        self._last_parameter_unit = ""
        self._modelKey = model_key
        self._base_url = Model.BASE_URL
        if base_url is not None:
            self._base_url = base_url

    @property
    def last_parameter_unit(self):
        return self._last_parameter_unit

    def bldg_geo(self):
        url = self._base_url + 'IDF3DViewerSocket.html'
        track = 'model_api_key'
        test = self._modelKey.split('-')
        if len(test) is 3:
            track = 'tracking'

        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
        }

        r = requests.get(url, params=payload)
        webbrowser.open(r.url)

    def bldg_orientation(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'Orientation'
        }

        r = requests.get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            self._last_parameter_unit = 'deg'

            return value
        else:
            return -1

    def num_above_ground_floor(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'BuildingStories'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            self._last_parameter_unit = 'floor'
            return data['total_cond_floor']
        else:
            return -1

    def num_total_floor(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'BuildingStories'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            self._last_parameter_unit = 'floor'
            return data['total_floor']
        else:
            return -1

    def num_zones(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'TotalZoneNumber'
        }

        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            self._last_parameter_unit = 'zones'
            return data['value']
        else:
            return -1

    def num_condition_zones(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'ConditionedZoneNumber'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            self._last_parameter_unit = 'zones'
            return data['value']
        else:
            return -1

    def condition_floor_area(self, unit):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'ConditionedZoneFloorArea'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
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
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'ZoneFloorArea'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = float(data['value'])
            self._last_parameter_unit = 'm2'

            if unit == 'ip':
                self._last_parameter_unit="ft2"
                value = value * 10.7639
            return value
        else:
            return -1

    def window_wall_ratio(self):
        url = self._base_url + 'GetBuildingBasicInfo_API'
        track = "folder_api_key"
        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"
        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey,
            'request_data': 'TotalWindowToWallRatio'
        }
        r = requests.get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            self._last_parameter_unit = ""

            return value
        else:
            return -1

    def zone_load(self, zone_name=None):
        url = self._base_url + 'GetZoneLoadInfo_API'
        track = "folder_api_key"

        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._userKey,
            track: self._modelKey
        }

        if zone_name is not None:
            payload['zone_name'] = zone_name

        r = requests.get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
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

        test = self._modelKey.split("-")
        if len(test) is 3:
            track = "track_token"

        payload = {
            'user_api_key': self._userKey,
             track: self._modelKey,
            'request_data': request_data
        }

        r = requests.get(url, params = payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        if resp_json['status'] == 'success':
            data = resp_json['data']
            value = data['value']
            if 'unit' in data:
                self._last_parameter_unit = data['unit']
            return value
        else:
            return -1
