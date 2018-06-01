"""
This post-process class shows the integration of parametric results with plotly.
Plotly is an open-source project that can be found in: https://plot.ly

It is required to have the latest plotly python package in your python.

"""
import os
import math

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class HTMLTable(object):

    def __init__(self, data):
        """
        Construct parametric plot

        :param data: returned from the parametric result call
        """

        self._data = data['data']['array']

        # construct the 2d dictionary - col - row - val
        data_dict = dict(dict())
        self._unit_dict = dict(dict())
        for i in range(len(self._data)):
            js = self._data[i]
            row = js['row']
            col = js['col']
            val_str = js['value']
            unit = js['unit']

            if row.isspace():
                continue
            if col.isspace():
                continue

            try:
                val = float(val_str)
            except ValueError:
                val = 0.0

            if row not in data_dict:
                data_dict[row] = dict()
            data_dict[row][col] = val

            if row not in self._unit_dict:
                self._unit_dict[row] = dict()
            self._unit_dict[row][col] = unit

        self._df = pd.DataFrame.from_dict(data_dict, orient='index')

    def pandas_df(self):
        return self._df

    def table_bar_chart_plot(self, orientation='column', title='Table bar plot', image_name='bar_table', skip_rows=None,
                             skip_cols=None):
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')
            return

        data = list()
        # based on orientations - change the for loop structure
        if orientation == 'column':
            for col in self._df:
                # skip this column
                if skip_cols is not None and col in skip_cols:
                    continue

                col_sum = 0
                unit = ''
                col_name_list = []
                row_val_list = []

                for index, row in self._df.iterrows():
                    # skip this row
                    if skip_rows is not None and index in skip_rows:
                        continue
                    # only include the none zero values
                    if row[col] > 0:
                        col_name_list.append(index)
                        row_val_list.append(row[col])
                    else:
                        continue

                    unit_temp = self._unit_dict[index][col]
                    if unit == '':
                        unit = unit_temp
                        col_sum = row[col]
                    elif unit == unit_temp:
                        col_sum = col_sum + row[col]
                    else:
                        col_name_list.pop()
                        row_val_list.pop()

                if col_sum > 0:
                    d = {
                        "x": col_name_list,
                        "y": row_val_list,
                        "name": col + ' (' + unit + ')',
                        "type": "bar"
                    }
                    data.append(d)
        elif orientation == 'row':
            for index, row in self._df.iterrows():
                # skip this row
                if skip_rows is not None and index in skip_rows:
                    continue

                row_sum = 0
                unit = ''
                col_name_list = []
                row_val_list = []

                for col in self._df:
                    if skip_cols is not None and col in skip_cols:
                        continue

                    # only include the none zero values
                    if row[col] > 0:
                        col_name_list.append(col)
                        row_val_list.append(row[col])
                    else:
                        continue

                    # exclude different unit col
                    unit_temp = self._unit_dict[index][col]
                    if unit == '':
                        unit = unit_temp
                        row_sum = row[col]
                    elif unit == unit_temp:
                        row_sum = row_sum + row[col]
                    else:
                        col_name_list.pop()
                        row_val_list.pop()

                if row_sum > 0:
                    d = {
                        "x": col_name_list,
                        "y": row_val_list,
                        "name": index + ' (' + unit + ')',
                        "type": "bar"
                    }
                    # a = {
                    #    "font":{
                    #        "size": 15
                    #    },
                    #    "showarrow": False,
                    #    "text": col
                    # }
                    data.append(d)
                    # annotation.append(a)
        # Check and decide the layout
        layout = dict(
            title=title,
            barmode='relative'
        )

        # layout['annotations'] = annotation
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fig = dict(data=data, layout=layout)
        plot(fig, filename=dir + '/' + image_name + '.html')

    def table_pie_chart_plot(self, orientation='column', title='Table pie plot', image_name='pie_table', skip_rows=None,
                             skip_cols=None):
        """
        plots rows and cols in pie chart -
        orientation indicates whether the legend of the chart is by column or by row
        only column and rows are accepted in this field
        :param orientation: only accept column or row
        :param title: the chart title
        :param image_name: the saved html name
        :param skip_rows: list of rows skip to plot
        :param skip_cols: list of cols skip to plot
        :return:
        """
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')
            return

        off_set = 0.02

        data = list()
        # based on orientations - change the for loop structure
        if orientation == 'column':
            for col in self._df:
                # skip the column
                if skip_cols is not None and col in skip_cols:
                    continue

                col_sum = 0
                unit = ''
                col_name_list = []
                row_val_list = []

                for index, row in self._df.iterrows():
                    # skip this row
                    if skip_rows is not None and index in skip_rows:
                        continue
                    # only include the none zero values
                    if row[col] > 0:
                        col_name_list.append(index)
                        row_val_list.append(row[col])
                    else:
                        continue

                    unit_temp = self._unit_dict[index][col]
                    if unit == '':
                        unit = unit_temp
                        col_sum = row[col]
                    elif unit == unit_temp:
                        col_sum = col_sum + row[col]
                    else:
                        col_name_list.pop()
                        row_val_list.pop()

                if col_sum > 0:
                    d = {
                        "values": row_val_list,
                        "labels": col_name_list,
                        "name": col + ' (' + unit + ')',
                        "hoverinfo": "label+percent+value+name",
                        "hole": .4,
                        "type": "pie"
                    }
                    # a = {
                    #     "font": {
                    #         "size": 15
                    #     },
                    #    "showarrow": False,
                    #    "text": col
                    # }
                    data.append(d)
                    # annotation.append(a)
        elif orientation == 'row':
            for index, row in self._df.iterrows():
                # skip this row
                if skip_rows is not None and index in skip_rows:
                    continue

                row_sum = 0
                unit = ''
                col_name_list = []
                row_val_list = []

                for col in self._df:
                    if skip_cols is not None and col in skip_cols:
                        continue

                    # only include the none zero values
                    if row[col] > 0:
                        col_name_list.append(col)
                        row_val_list.append(row[col])
                    else:
                        continue

                    # exclude different unit col
                    unit_temp = self._unit_dict[index][col]
                    if unit == '':
                        unit = unit_temp
                        row_sum = row[col]
                    elif unit == unit_temp:
                        row_sum = row_sum + row[col]
                    else:
                        col_name_list.pop()
                        row_val_list.pop()

                if row_sum > 0:
                    d = {
                        "values": row_val_list,
                        "labels": col_name_list,
                        "name": index + ' (' + unit + ')',
                        "hoverinfo": "label+percent+value+name",
                        "hole": .4,
                        "type": "pie"
                    }
                    # a = {
                    #    "font":{
                    #        "size": 15
                    #    },
                    #    "showarrow": False,
                    #    "text": col
                    # }
                    data.append(d)
                    # annotation.append(a)
        # Check and decide the layout
        size = len(data)
        p_row = math.ceil(size / 2)

        if size >= 2:
            for i in range(len(data)):
                d = data[i]
                x_l = 0 if i % 2 == 0 else 0.52
                x_u = 0.48 if i % 2 == 0 else 1
                y_u = 1 - (1 / p_row * (math.floor(i / 2) + 1) - off_set)
                y_l = 1 - 1 / p_row * (math.floor(i / 2))
                d['domain'] = {'x': [x_l, x_u], 'y': [y_l, y_u]}
                # a = annotation[i]
                # a['x'] = x_d-0.25
                # a['y'] = 1 - (y_u - y_l) / 2 + y_l

        layout = dict(
            title=title
        )

        # layout['annotations'] = annotation
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fig = dict(data=data, layout=layout)
        plot(fig, filename=dir + '/' + image_name + '.html')












