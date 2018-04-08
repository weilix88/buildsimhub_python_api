import requests
import webbrowser

# This is a class that contains all the model information for user
# to read


# potentially in the future, to write

class ParametricModel:
    # every call will connect to this base URL
    BASE_URL = 'https://my.buildsim.io/'

    def __init__(self, userKey, model_key, base_url=None):
        self._user_key = userKey
        self._last_parameter_unit = ""
        self._model_key = model_key
        self._base_url = ParametricModel.BASE_URL
        if base_url is not None:
            self._base_url = base_url

    @property
    def last_parameter_unit(self):
        return self._last_parameter_unit

    def bldg_geo(self):
        url = self._base_url + 'IDF3DViewerSocket.html'
        track = 'model_api_key'
        test = self._model_key.split('-')
        if len(test) is 3:
            track = 'tracking'

        payload = {
            'user_api_key': self._user_key,
            track: self._model_key,
        }

        r = requests.get(url, params=payload)
        webbrowser.open(r.url)

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
        url = self._base_url + 'ParametricResults_API'
        payload = {
            'user_api_key': self._user_key,
            'folder_api_key': self._model_key,
            'request_data': request_data
        }

        r = requests.get(url, params=payload)
        resp_json = r.json()
        if r.status_code > 200:
            print('Code: ' + r.status_code + ' message: ' + resp_json['error_msg'])
            return False

        value = list()
        model = list()
        model_plot = list()
        counter = 1
        if resp_json['status'] == 'success':
            datalist = resp_json['data']
            for i in range(len(datalist)):
                value.append(datalist[i]['value'])
                model.append(datalist[i]['model'])
                model_plot.append('case' + str(counter))
                counter += 1
                if 'unit' in datalist[i]:
                    self._lastParameterUnit = datalist[i]['unit']
            result = dict()
            result['value'] = value
            result['model'] = model
            result['model_plot'] = model_plot
            return result
        else:
            return resp_json['error_msg']
