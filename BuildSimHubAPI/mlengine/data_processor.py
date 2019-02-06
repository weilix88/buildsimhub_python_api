import BuildSimHubAPI as bsh_api
import pandas as pd
from enum import Enum


class DataRequester(object):
    def __init__(self):
        '''

        :param request_data:
        :type request_data: RequestData
        '''
        self._df = None

    def get_df(self):
        return self._df

    def add_column_with_request(self, project_api_key, model_api_key, request, base_url=None):
        if base_url is None:
            bsh = bsh_api.BuildSimHubAPIClient()
        else:
            bsh = bsh_api.BuildSimHubAPIClient(base_url)

        if not isinstance(request, RequestData):
            raise Exception('Request data need to be the RequestData')

        param = bsh.parametric_results(project_api_key, model_api_key)
        results = self.__call_function(request, param)
        result_unit = param.last_parameter_unit
        temp_list = results['model']
        result_dict = dict()
        for i in range(len(temp_list)):
            tempstr = results['model'][i]
            templist = tempstr.split(',')
            for j in range(len(templist)):
                pair = templist[j].split(": ")
                key = pair[0].strip()
                if key not in result_dict:
                    result_dict[key] = []
                result_dict[key].append(pair[1])
        temp_list = results['value']
        temp_name = request.name + ' (' + result_unit + ')'
        result_dict[temp_name] = []
        for i in range(len(temp_list)):
            result_dict[temp_name].append(temp_list[i])

        if self._df is None:
            self._df = pd.DataFrame(result_dict)
        else:

            temp_df = pd.DataFrame(result_dict)
            self._df[temp_name] = temp_df[temp_name]
            print(self._df.to_string())

    def retrieve_headers(self):
        return list(self._df)

    def set_datatype_num(self, headers):
        self._df[headers] = self._df[headers].apply(pd.to_numeric, errors='coerce')

    def retrieve_data(self, project_api_key, model_api_key, request, base_url=None):
        """
        Retrieve the data from different parametric models with the same set of
        parameters (no guarantee that different parameters will be working)

        :param project_api_key:
        :param model_api_key:
        :param request
        :param base_url:
        :return:
        """
        if base_url is None:
            bsh = bsh_api.BuildSimHubAPIClient()
        else:
            bsh = bsh_api.BuildSimHubAPIClient(base_url)

        if not isinstance(request, RequestData):
            raise Exception('Request data need to be the RequestData')

        param = bsh.parametric_results(project_api_key, model_api_key)

        results = self.__call_function(request, param)
        result_unit = param.last_parameter_unit

        temp_list = results['model']
        result_dict = dict()
        for i in range(len(temp_list)):
            tempstr = results['model'][i]
            templist = tempstr.split(',')
            for j in range(len(templist)):
                pair = templist[j].split(": ")
                key = pair[0].strip()
                if key not in result_dict:
                    result_dict[key] = []
                result_dict[key].append(pair[1])
        temp_list = results['value']
        temp_name = request.name + ' (' + result_unit + ')'
        result_dict[temp_name] = []
        for i in range(len(temp_list)):
            result_dict[temp_name].append(temp_list[i])

        if self._df is None:
            self._df = pd.DataFrame(result_dict)
        else:
            base_df = self._df
            temp_df = pd.DataFrame(result_dict)
            self._df = pd.concat([base_df, temp_df], ignore_index=True)

    def data_describe(self):
        if self._df is None:
            return 'No data available'
        else:
            return self._df.describe(include='all')

    @staticmethod
    def __call_function(request, parametric):
        val = request.value
        results = None
        if val == 1:
            results = parametric.bldg_load('heating')
        elif val == 2:
            results = parametric.bldg_load('cooling')
        elif val == 3:
            results = parametric.net_site_eui()
        elif val == 4:
            results = parametric.total_site_eui()
        elif val == 5:
            results = parametric.not_met_hour_cooling()
        elif val == 6:
            results = parametric.not_met_hour_heating()
        elif val == 7:
            results = parametric.total_end_use_electricity()
        elif val == 8:
            results = parametric.total_end_use_naturalgas()
        elif val == 9:
            results = parametric.cooling_electricity()
        elif val == 10:
            results = parametric.domestic_hotwater_electricity()
        elif val == 11:
            results = parametric.domestic_hotwater_naturalgas()
        elif val == 12:
            results = parametric.exetrior_equipment_electricity()
        elif val == 13:
            results = parametric.exterior_equipment_naturalgas()
        elif val == 14:
            results = parametric.exterior_lighting_electricity()
        elif val == 15:
            results = parametric.fan_electricity()
        elif val == 16:
            results = parametric.heating_electricity()
        elif val == 17:
            results = parametric.heating_naturalgas()
        elif val == 18:
            results = parametric.heat_rejection_electricity()
        elif val == 19:
            results = parametric.interior_equipment_electricity()
        elif val == 20:
            results = parametric.interior_equipment_naturalgas()
        elif val == 21:
            results = parametric.interior_lighting_electricity()
        elif val == 22:
            results = parametric.pumps_electricity()
        elif val == 23:
            results = parametric.bldg_lpd()
        elif val == 24:
            results = parametric.bldg_epd()
        elif val == 25:
            results = parametric.bldg_ppl()
        elif val == 26:
            results = parametric.wall_rvalue()
        elif val == 27:
            results = parametric.roof_rvalue()
        elif val == 28:
            results = parametric.window_uvalue()
        elif val == 29:
            results = parametric.window_shgc()
        elif val == 30:
            results = parametric.roof_absorption()
        elif val == 31:
            results = parametric.bldg_water_heater_efficiency()
        elif val == 32:
            results = parametric.bldg_dx_cooling_efficiency()
        elif val == 33:
            results = parametric.bldg_chiller_efficiency()
        elif val == 34:
            results = parametric.bldg_electric_boiler_efficiency()
        elif val == 35:
            results = parametric.bldg_fuel_boiler_efficiency()
        elif val == 36:
            results = parametric.bldg_dx_heating_efficiency()
        elif val == 37:
            results = parametric.bldg_sys_loads('heating')
        elif val == 38:
            results = parametric.bldg_sys_loads('cooling')
        return results


class RequestData(Enum):
    bldg_heat_load = 1
    bldg_cool_load = 2
    net_site_eui = 3
    total_site_eui = 4
    not_met_hour_cooling = 5
    not_met_hour_heating = 6
    total_end_use_electricity = 7
    total_end_use_naturalgas = 8
    cooling_electricity = 9
    domestic_hotwater_electricity = 10
    domestic_hotwater_naturalgas = 11
    exetrior_equipment_electricity = 12
    exterior_equipment_naturalgas = 13
    exterior_lighting_electricity = 14
    fan_electricity = 15
    heating_electricity = 16
    heating_naturalgas = 17
    heat_rejection_electricity = 18
    interior_equipment_electricity = 19
    interior_equipment_naturalgas = 20
    interior_lighting_electricity = 22
    pumps_electricity = 22
    bldg_lpd = 23
    bldg_epd = 24
    bldg_ppl = 25
    wall_rvalue = 26
    roof_rvalue = 27
    window_uvalue = 28
    window_shgc = 29
    roof_absorption = 30
    bldg_water_heater_efficiency = 31
    bldg_dx_cooling_efficiency = 32
    bldg_chiller_efficiency = 33
    bldg_electric_boiler_efficiency = 34
    bldg_fuel_boiler_efficiency = 35
    bldg_dx_heating_efficiency = 36
    bldg_sys_heating_load = 37
    bldg_sys_cooling_load = 38
