

class ModelAction(object):

    def __init__(self, name, unit='si'):
        """
        Construct a ModelAction - a model action is a measure

        :param name:
        :param unit: choose between si or ip, default is si
        """
        # type: (str, str) -> ModelAction
        self._list_data = list()
        self._data = None
        self._unit = unit
        self._name = name
        self._default_list = []
        self._min = 0
        self._max = 0

    def unit(self):
        """Returns the unit system (si or ip)"""
        return self._unit

    def num_of_value(self):
        return len(self._list_data)

    def set_min(self, min_val):
        self._min = min_val

    def set_max(self, max_val):
        self._max = max_val

    def get_data_string(self):
        if not self._list_data:
            return "[" + ",".join(str(x) for x in self._default_list) + "]"
        else:
            return "[" + ",".join(str(x) for x in self._list_data) + "]"

    def get_datalist(self):
        return self._list_data

    def get_data(self):
        return "[" + str(self._data) + "]"

    def get_boundary(self):
        return "[" + str(self._min) + "," + str(self._max) + "]"

#    def num_of_combinations(self):
#        comb = 0
#        for i in range(len(self._list_data)):
#            data_list = self._list_data[i]
#            if(comb == 0):
#                comb = len(data_list)
#            else:
#                comb = comb * len(data_list)
#        return comb

    def set_datalist(self, data_list):
        self._list_data = data_list
        return True

    def set_data(self, data):
        self._data = data
        return True

    def get_api_name(self):
        return self._name
