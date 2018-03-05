try:
    import matplotlib.pyplot as plt
except ImportError:
    print('matplotlib is not installed')

try:
    import numpy as np
except ImportError:
    print('numpy is not installed')


class ParametricPlot:
    def __init__(self, data, unit=""):
        self._value = data['value']
        self._unit = unit

        self._model_plot = data['model_plot']
        model_des = data['model']

        data = list()
        column = list()

        first_col = model_des[0]

        # create the column and first row of data
        parameters = first_col.split(",")
        first_set_data = list()
        for i in range(len(parameters)):
            title, val = parameters[i].split(":")
            column.append(title)
            first_set_data.append(val)
        data.append(first_set_data)

        # fill up with all the values
        for j in range(1, len(model_des)):
            parameters = model_des[j].split(",")
            data_set = list()
            for k in range(len(parameters)):
                title, val = parameters[k].split(":")
                data_set.append(val)
            data.append(data_set)

        # list of headers
        self._col = column
        # 2d list, [[row],[row]]
        self._data_table = data

    def line_plot(self, title):
        ind = np.arange(len(self._value))
        plt.pyplot.xticks(ind, self._model_plot)
        plt.pyplot.plot(self._value)
        plt.pyplot.ylabel(self._unit)
        plt.title(title)
        plt.pyplot.show()


