"""
OneZoneLoad class - post-process a zone load's data
and form it into a pandas dataframe
"""

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class OneZoneLoad(object):
    def __init__(self, one_zone_load_profile):
        zone_load = one_zone_load_profile[0]
        self._zone_name = zone_load['zone_name']
        self._floor_area = zone_load['floor_area']
        self._floor_area_unit = zone_load['floor_area_unit']
        data = zone_load['data']
        self._cooling_load_unit = data['cooling_unit']
        self._heating_load_unit = data['heating_unit']

        self._cooling_load_list = data['cooling']
        self._heating_load_list = data['heating']

    @property
    def zone_name(self):
        return self._zone_name

    @property
    def floor_area(self):
        return self._floor_area

    @property
    def floor_area_unit(self):
        return self._floor_area_unit

    @property
    def cooling_load_unit(self):
        return self._cooling_load_unit

    @property
    def heating_load_unit(self):
        return self._heating_load_unit

    def cooling_load_table(self):
        """
        This method returns the full cooling load table in pandas data frame
        :return:
        """
        data = list()
        index_list = list()
        for d_dict in self._cooling_load_list:
            data_dict = dict()

            if d_dict['load_component'] == 'Grand Total':
                continue

            index_list.append(d_dict['load_component'])
            data_dict['Sensible - Instant'] = d_dict['Sensible - Instant']
            data_dict['Sensible - Delayed'] = d_dict['Sensible - Delayed']
            data_dict['Sensible - Return Air'] = d_dict['Sensible - Return Air']
            data_dict['Latent'] = d_dict['Latent']
            data_dict['Total'] = d_dict['Total']
            data_dict['Total per Area'] = d_dict['Total per Area']
            data_dict['%Grand Total'] = d_dict['%Grand Total']
            data_dict['Related Area'] = d_dict['Related Area']

            data.append(data_dict)
        return pd.DataFrame(data, index=index_list)

    def heating_load_table(self):
        """
        This table returns the full heating load table in pandas data frame
        :return:
        """
        data = list()
        index_list = list()
        for d_dict in self._heating_load_list:
            data_dict = dict()

            if d_dict['load_component'] == 'Grand Total':
                continue

            index_list.append(d_dict['load_component'])
            data_dict['Sensible - Instant'] = d_dict['Sensible - Instant']
            data_dict['Sensible - Delayed'] = d_dict['Sensible - Delayed']
            data_dict['Sensible - Return Air'] = d_dict['Sensible - Return Air']
            data_dict['Latent'] = d_dict['Latent']
            data_dict['Total'] = d_dict['Total']
            data_dict['Total per Area'] = d_dict['Total per Area']
            data_dict['%Grand Total'] = d_dict['%Grand Total']
            data_dict['Related Area'] = d_dict['Related Area']

            data.append(data_dict)
        return pd.DataFrame(data, index=index_list)

    def cooling_load_component_total(self):
        """
        This function returns total values for the cooling load component
        It includes total and total per area

        :return:
        """
        data = list()
        index_list = list()
        for d_dict in self._cooling_load_list:
            data_dict = dict()

            if d_dict['load_component'] == 'Grand Total':
                continue

            index_list.append(d_dict['load_component'])
            data_dict['Total'] = d_dict['Total']
            data_dict['Total per Area'] = d_dict['Total per Area']
            data.append(data_dict)
        return pd.DataFrame(data, index=index_list)

    def heating_load_component_total(self):
        """
        This function returns total values for the heating load component
        It includes total and total per area

        :return:
        """
        data = list()
        index_list = list()
        for d_dict in self._heating_load_list:
            data_dict = dict()

            if d_dict['load_component'] == 'Grand Total':
                continue

            index_list.append(d_dict['load_component'])
            data_dict['Total'] = d_dict['Total']
            data_dict['Total per Area'] = d_dict['Total per Area']
            data.append(data_dict)
        return pd.DataFrame(data, index=index_list)

    def cooling_load_component_detail(self):
        """
        This function returns detail values for the cooling load component
        It includes sensible - instant, sensible - delayed, sensible - return air and latent load

        :return:
        """
        data = list()
        index_list = list()
        for d_dict in self._cooling_load_list:
            data_dict = dict()

            if d_dict['load_component'] == 'Grand Total':
                continue

            index_list.append(d_dict['load_component'])
            data_dict['Sensible - Instant'] = d_dict['Sensible - Instant']
            data_dict['Sensible - Delayed'] = d_dict['Sensible - Delayed']
            data_dict['Sensible - Return Air'] = d_dict['Sensible - Return Air']
            data_dict['Latent'] = d_dict['Latent']
            data.append(data_dict)
        return pd.DataFrame(data, index=index_list)

    def heating_load_component_detail(self):
        """
        This function returns detail values for the heating load component
        It includes sensible - instant, sensible - delayed, sensible - return air and latent load

        :return:
        """
        data = list()
        index_list = list()
        for d_dict in self._heating_load_list:
            data_dict = dict()

            if d_dict['load_component'] == 'Grand Total':
                continue

            index_list.append(d_dict['load_component'])
            data_dict['Sensible - Instant'] = d_dict['Sensible - Instant']
            data_dict['Sensible - Delayed'] = d_dict['Sensible - Delayed']
            data_dict['Sensible - Return Air'] = d_dict['Sensible - Return Air']
            data_dict['Latent'] = d_dict['Latent']
            data.append(data_dict)
        return pd.DataFrame(data, index=index_list)
