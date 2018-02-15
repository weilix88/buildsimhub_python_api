import requests
import json

#This is a class that contains all the model information for user
#to read


#potentially in the future, to write

class Model():
    #every call will connect to this base URL
    BASE_URL = 'https://develop.buildsimhub.net/'

    def __init__(self, userKey, modelKey):
        self._userKey = userKey
        self._modelKey = modelKey

    def bldg_orientation(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'Orientation'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def num_above_ground_floor(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'BuildingStories'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            return data['total_cond_floor']
        else:
            return resp_json['error_msg']

    def num_total_floor(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'BuildingStories'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            return data['total_floor']
        else:
            return resp_json['error_msg']

    def num_zones(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'TotalZoneNumber'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            return data['value']
        else:
            return resp_json['error_msg']

    def num_condition_zones(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'ConditionedZoneNumber'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            return data['value']
        else:
            return resp_json['error_msg']


    def condition_floor_area(self, unit):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'ConditionedZoneFloorArea'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = float(data['value'])
            if(unit=='ip'):
                value = value * 10.7639
            return value
        else:
            return -1

    def gross_floor_area(self, unit):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'ZoneFloorArea'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = float(data['value'])
            if(unit=='ip'):
                value = value * 10.7639
            return value
        else:
            return -1

    def window_wall_ratio(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'TotalWindowToWallRatio'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    #Below are the methods use for retrieving results
    def net_site_eui(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'NetSiteEUI'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def total_site_eui(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'TotalSiteEUI'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def not_met_hour_cooling(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'NotMetHoursCooling'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def not_met_hour_heating(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'NotMetHoursHeating'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def not_met_hour_total(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'NotMetHoursTotal'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def total_end_use_electricity(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'TotalEndUseElectricity'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def total_end_use_naturalgas(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'TotalEndUseNaturalGas'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def cooling_electricity(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'CoolingElectricity'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def cooling_naturalgas(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'CoolingNaturalGas'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def domestic_hotwater_electricity(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'DomesticHotWaterElectricity'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1

    def domestic_hotwater_naturalgas(self):
        url = Model.BASE_URL + 'GetBuildingSimulationResults_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'DomesticHotWaterNaturalGas'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1