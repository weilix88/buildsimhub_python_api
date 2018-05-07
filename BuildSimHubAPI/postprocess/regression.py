
try:
    import numpy as np
except ImportError:
    np = None
    print('numpy is not installed')

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class Regression(object):
    def __init__(self, data, unit=""):
        """
        Construct parametric plot

        :param data: returned from the parametric result call
        :param unit:
        """
        self._value = data['value']
        self._unit = unit

        self._model_plot = data['model_plot']
        self._model_des = data['model']

        data_list = list()

        # create data dictionary
        for j in range(len(self._model_des)):
            col_list = self._model_des[j]
            parameters = col_list.split(",")
            data_dict = dict()
            for k in range(len(parameters)):
                title, val = parameters[k].split(":")
                # for cases like on off options
                if val.strip() == 'Off':
                    val = '0'
                if val.strip() == 'On':
                    val = '1'

                data_dict[title.strip()] = float(val.strip())
            # data_dict['Value'] = self._value[j]

            data_list.append(data_dict)

        self._df = pd.DataFrame(data_list, index=self._model_plot)
        self._df['Value'] = self._value

    def pandas_df(self):
        """get the data in pandas dataframe"""
        return self._df

    def add_column(self, head, col):
        """

        :param head:
        :param col:
        :type head: str
        :type col: list
        :return:
        """
        if head == 'Value':
            return False
        self._df.assign(head=col)

    def x_validate(self):
        y = self._df[['Value']]
        try:
            from sklearn.model_selection import cross_val_score
        except ImportError:
            print("Sci-kit learn package is required for model training. Please install the package at: "
                  "http://scikit-learn.org/stable/index.html")
            return

        




