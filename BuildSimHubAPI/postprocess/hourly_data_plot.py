"""
This post-process class shows the integration of hourly data results with plotly.
Plotly is an open-source project that can be found in: https://plot.ly

It is required to have the latest plotly python package in your python.

"""
import os
import datetime as datetime

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class HourlyPlot(object):

    def __init__(self, data, variable_name=''):
        """
        Construct parametric plot

        :param data: returned from the parametric result call
        """
        self._variable_name = variable_name
        self._resolution = data['resolution']
        self._category = data['category']
        self._unit_prime = data['unit']
        self._unit_sec = ''
        self._data = data['data']
        self._col_unit_dict = dict()

        data_list = list()

        # create data dictionary
        for j in range(len(self._data)):
            data_dict = dict()
            data_time = self._data[j]

            time_step = data_time['timestamp']
            format_time = self.__date_time_str(time_step)
            date = datetime.datetime.strptime(format_time, '%m/%d/%Y %H:%M:%S')
            # col_list.append(date)
            data_dict['timestamp'] = date
            data_dict[variable_name] = float(data_time['value'])
            data_list.append(data_dict)

        self._col_unit_dict[variable_name] = self._unit_prime
        self._df = pd.DataFrame(data_list)

    def add_column(self, data, variable_name):
        resolution = data['resolution']
        if resolution != self._resolution:
            print("Cannot add data resolution " + resolution + "to the primary data resolution: " + self._resolution)
            return False

        unit = data['unit']
        assert isinstance(self._unit_prime, object)

        if unit != self._unit_prime:
            if self._unit_sec == '':
                # add to the unit dict
                self._unit_sec = unit
                self._col_unit_dict[variable_name] = self._unit_sec
            elif unit == self._unit_sec:
                self._col_unit_dict[variable_name] = self._unit_sec
            else:
                print("No more than two dimensions data frame allowed in line chart")
                return False
        else:
            self._col_unit_dict[variable_name] = self._unit_prime

        data_list = list()
        data_array = data['data']
        for i in range(len(data_array)):
            data_list.append(float(data_array[i]['value']))

        self._df[variable_name] = data_list
        return True

    def pandas_df(self):
        """get the data in pandas dataframe"""
        return self._df

    def heat_map_plot(self, image_name="test", color_scale='Viridis'):
        """Plotly heat map plot
        Only plot the first column data
        on the heat map -
        """
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')
            return

        heat_map_df = self._df.copy()
        heat_map_df['date'] = [d.date() for d in heat_map_df['timestamp']]
        heat_map_df['time'] = [d.time() for d in heat_map_df['timestamp']]

        data = list()
        trace = go.Heatmap(z=heat_map_df[self._variable_name],
                           x=heat_map_df['time'],
                           y=heat_map_df['date'],
                           colorscale=color_scale)
        data.append(trace)

        layout = go.Layout(
            title=self._variable_name + ' (' + self._unit_prime + ')',
            yaxis=dict(ticks='', nticks=36)
        )

        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fig = dict(data=data, layout=layout)
        plot(fig, filename=dir + '/' + image_name + '.html')

    def line_chart_plot(self, image_name='test'):
        """
        This works for all the values in the df

        :return:
        """
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')
            return

        data = list()
        time_col = self._df['timestamp']
        for column in self._df:
            if column == 'timestamp':
                continue
            unit_temp = self._col_unit_dict[column]
            if unit_temp == self._unit_prime:
                trace = go.Scatter(
                    name=column + ' (' + unit_temp + ')',
                    mode='lines',
                    x=time_col,
                    y=self._df[column]
                )
            elif unit_temp == self._unit_sec:
                trace = go.Scatter(
                    name=column + ' (' + unit_temp + ')',
                    mode='lines',
                    x=time_col,
                    y=self._df[column],
                    yaxis='y2'
                )
            data.append(trace)

        layout = dict(
            title='Line plot',
            yaxis=dict(
                title=self._unit_prime
            ),
            legend=dict(orientation='h')
        )

        if self._unit_sec != '':
            yaxis2 = dict()
            yaxis2['title'] = self._unit_sec
            yaxis2['overlaying'] = 'y'
            yaxis2['side'] = 'right'
            layout['yaxis2'] = yaxis2

        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fig = dict(data=data, layout=layout)
        plot(fig, filename=dir + '/' + image_name + '.html')

    @staticmethod
    def __date_time_str(dt):
        """
        reformat the date_tiem string
        example: 1/1/2018 01:00:00 -> 1/1/2018 00:00:00
        :param dt:
        :return:
        """

        date_time_item = dt.split(' ')
        date_str = date_time_item[0]

        time_str = date_time_item[1]
        time_item = time_str.split(':')

        hr = time_item[0]
        hr_int = int(hr)
        hr_int = hr_int-1

        return date_str + ' ' + str(hr_int)+':' + time_item[1] + ':' + time_item[2]

