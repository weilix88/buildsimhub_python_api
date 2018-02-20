import requests
import json
from .simulationJob import SimulationJob

#This is a class that contains all the model information for user
#to read


#potentially in the future, to write

class HTMLResults():
    #every call will connect to this base URL
    BASE_URL = 'https://develop.buildsimhub.net/'

    def __init__(self, userKey, simulationJob):
        self._userKey = userKey
        self._modelKey = simulationJob.modelKey
        self._lastParameterUnit = ''

    @property
    def lastParameterUnit(self):
        return self._lastParameterUnit

    def request_numeric_value(self, report, table, column_name, row_name):
        url = HTMLResults.BASE_URL + 'GetNumericValueFromHTML_API'
        payload = {
            'user_api_key': self._userKey,
            'track_token': self._modelKey,
            'report': report,
            'table': table,
            'column_name': column_name,
            'row_name': row_name
        }

        r = request.get(url, params = payload)
        resp_json = r.json()
        if(resp_json['status']=='success'):
            data = resp_json['data']
            value = data['value']
            if('unit' in data):
                self._lastParameterUnit = data['unit']
            else:
                self._lastParameterUnit = ''
            return value
        else:
            return -1