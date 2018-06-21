"""
BuildingLoad class - post-process bldg level load data
and form it into a pandas dataframe
"""

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class BuildingLoad(object):

    def __init__(self, bldg_load_profile):
        """
        
        :param bldg_load_profile: bldg_load_profile: jsonarray returned
            from BSH server by calling the building load api
        """

        # reform the dict
        index_list = list()
        self._cooling_unit = ''
        self._heating_unit = ''
        self._cooling_density_unit = ''
        self._heating_density_unit = ''
        data = list()
        for d_dict in bldg_load_profile:
            data_dict = dict()
            if len(d_dict.keys()) == 1:
                continue
            index_list.append(d_dict['model'].upper())
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
            data_dict['cooling_load'] = d_dict['cooling_load']
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

    def pandas_df(self):
        """get the dataframe"""
        return self._df

    def plot(self):
        """Plotly scatter plot"""
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')

        data = list()
