try:
    import pandas as pd
except ImportError:
    print('pandas is not installed')


class ZoneLoad:
    def __init__(self, load_profile):
        # reform the dict
        index_list = list()
        self._cooling_unit = ''
        self._heating_unit = ''
        self._cooling_density_unit = ''
        self._heating_density_unit = ''
        data = list()
        for d_dict in load_profile:
            data_dict = dict()
            if len(d_dict.keys()) == 1:
                continue
            index_list.append(d_dict['zone_name'].upper())
            if self._cooling_unit == '':
                self._cooling_unit = d_dict['cooling_unit']
            if self._heating_unit == '':
                self._heating_unit = d_dict['heating_unit']
            if self._heating_density_unit == '':
                self._heating_density_unit = d_dict['heating_load_density_unit']
            if self._cooling_density_unit == '':
                self._cooling_density_unit = d_dict['cooling_load_density_unit']
            # remove name and units from the dict
            data_dict['heating_load'] = d_dict['heating_load']
            data_dict['heating_peak_load_time'] = d_dict['heating_peak_load_time']
            data_dict['cooling_load'] = d_dict['cooling_load']
            data_dict['cooling_peak_load_time'] = d_dict['cooling_peak_load_time']
            data_dict['heating_load_density'] = d_dict['heating_load_density']
            data_dict['cooling_load_density'] = d_dict['cooling_load_density']
            data.append(data_dict)
        self._df = pd.DataFrame(data, index=index_list)

    @property
    def cooling_load_unit(self):
        return self._cooling_unit

    @property
    def heating_load_unit(self):
        return self._heating_unit

    @property
    def cooling_load_density_unit(self):
        return self._cooling_density_unit

    @property
    def heating_load_density_unit(self):
        return self._heating_density_unit

    def get_df(self):
        return self._df

    def get_zone_heat_load(self, zone):
        zone_name = zone.upper()
        return self._df.at[zone_name, 'heating_load']

    def get_zone_cool_load(self, zone):
        zone_name = zone.upper()
        return self._df.at[zone_name, 'cooling_load']

    def get_zone_heat_load_time(self, zone):
        zone_name = zone.upper()
        return self._df.at[zone_name, 'heating_peak_load_time']

    def get_zone_cool_load_time(self, zone):
        zone_name = zone.upper()
        return self._df.at[zone_name, 'cooling_peak_load_time']

# sample test data
#test_data = [{'zone_name': 'SPACE1-1', 'heating_unit': 'W', 'cooling_unit': 'W', 'heating_load': '-7804.11',
#              'cooling_load': '7389.08', 'cooling_peak_load_time': '7/21/15:45:00', 'heating_peak_load_time': '1/21 24:00:00'},
#             {'zone_name': 'SPACE5-1', 'heating_unit': 'W', 'cooling_unit': 'W', 'heating_load': '-6165.32',
#              'cooling_load': '8335.26', 'cooling_peak_load_time': '7/21/15:00:00',
#              'heating_peak_load_time': '1/21 24:00:00'}
#             ]

# zl = ZoneLoad(test_data)
# print(zl.get_zone_heat_load('space1-1'))
# print(zl.get_zone_cool_load('space5-1'))
