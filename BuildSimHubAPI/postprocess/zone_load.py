"""
ZoneLoad class - post-process zone load data
and form it into a pandas dataframe
"""
import os

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class ZoneLoad(object):
    def __init__(self, load_profile):
        """
        Construct zoneload class

        :param load_profile: data returned from zone_load api call
        """
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

    def pandas_df(self):
        """get the dataframe"""
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

    def load_bar_chart_plot(self, mode='default', image_name='test'):
        """Plotly bar chart plot
            plots all the zone's cooling and heating load components
        """
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')
            return

        data = list()

        if mode == 'density':
            heat_trace = go.Bar(
                x=self._df.index,
                y=self._df['heating_load_density'],
                name='Heating Load' + ' (' + self._heating_density_unit + ')',
                marker=dict(
                    color='rgb(178,34,34)'
                )
            )

            cool_trace = go.Bar(
                x=self._df.index,
                y=self._df['cooling_load_density'],
                name='Cooling Load' + ' (' + self._cooling_density_unit + ')',
                marker=dict(
                    color='rgb(26, 118, 255)'
                )
            )
            data.append(heat_trace)
            data.append(cool_trace)
        else:
            heat_trace = go.Bar(
                x=self._df.index,
                y=self._df['heating_load'],
                name='Heating Load' + ' (' + self._heating_unit + ')',
                marker=dict(
                    color='rgb(178,34,34)'
                )
            )

            cool_trace = go.Bar(
                x=self._df.index,
                y=self._df['cooling_load'],
                name='Cooling Load' + ' (' + self._cooling_unit + ')',
                marker=dict(
                    color='rgb(26, 118, 255)'
                )
            )
            data.append(heat_trace)
            data.append(cool_trace)

        layout = dict(
            title='Test',
            barmode='relative'
        )
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fig = dict(data=data, layout=layout)
        plot(fig, filename=dir + '/' + image_name + '.html')
