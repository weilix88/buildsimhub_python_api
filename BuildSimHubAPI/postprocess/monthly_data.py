"""
This post-process class shows the integration of monthly data results with pandas.

"""
import os
import datetime as datetime

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class MonthlyTable(object):

    def __init__(self, data):
        print(data)
        column_meta = data['columnMeta']
        data_list = list()
        row_list = list()
        column_list = list()
        for key in column_meta:
            column_list.append(key)

        data_array = data['data']
        for i in range(len(data_array)):
            data_cell = data_array[i]
            if data_cell[0] == '\xa0':
                # this means no data - or empty
                continue
            row_list.append(data_cell[0])
            data_dict = dict()
            for j in range(1, len(data_cell)):
                data_dict[column_list[j-1]] = data_cell[j]
            data_list.append(data_dict)

        self._df = pd.DataFrame(data_list, index=row_list)

    def pandas_df(self):
        return self._df
