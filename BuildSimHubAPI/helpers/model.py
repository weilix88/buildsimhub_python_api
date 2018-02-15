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

    def numberOfAboveGroundFloors(self):
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

    def numberOfTotalFloors(self):
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

    def numberOfZones(self):
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

    def numberOfConditionedZones(self):
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


    def conditionedFloorArea(self, unit):
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

    def grossFloorArea(self, unit):
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
            value = data['value']
            #if(unit=='ip'):
            #    value = value * 10.7639
            return value
        else:
            return -1

    def windowToWallRatio(self):
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

    def weatherFileName(self):
        url = Model.BASE_URL + 'GetBuildingBasicInfo_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'request_data': 'WeatherFileName'
        }
        r = requests.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status'] == 'success'):
            data = resp_json['data']
            value = data['value']
            return value
        else:
            return -1
