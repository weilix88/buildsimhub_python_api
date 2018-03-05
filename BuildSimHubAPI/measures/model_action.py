

class ModelAction():
    def __init__(self, name, unit='ip'):
        # type: (str, str) -> ModelAction
        self._list_data = list()
        self._data = None
        self._unit = unit
        self._name = name

    def unit(self):
        return self._unit

    def num_of_value(self):
        return len(self._list_data)

    def get_data_string(self):
        return "["+",".join(str(x) for x in self._list_data)+"]"

    def get_datalist(self):
        return self._list_data

    def get_data(self):
        return data

#    def num_of_combinations(self):
#        comb = 0
#        for i in range(len(self._list_data)):
#            data_list = self._list_data[i]
#            if(comb == 0):
#                comb = len(data_list)
#            else:
#                comb = comb * len(data_list)
#        return comb

    def set_datalist(self, datalist):
        self._list_data = datalist

    def set_data(self, data):
        self._data = data

    def get_api_name(self):
        return self._name;



