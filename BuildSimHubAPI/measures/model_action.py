from BuildSimHubAPI.measures.design_template import DesignTemplate


class ModelAction(object):

    def __init__(self, name, unit='si'):
        """
        Construct a ModelAction - a model action is a measure

        :param name:
        :param unit: choose between si or ip, default is si
        """
        self._list_data = list()
        self._data = None
        self._unit = unit
        self._name = name
        self._default_list = list()
        self._upper_limit = float('inf')
        self._lower_limit = float('-inf')
        self._min = None
        self._max = None
        self._measure_name = "Default"
        self._measure_help = ''
        self._custom_template = list()

    def unit(self):
        """Returns the unit system (si or ip)"""
        return self._unit

    def num_of_value(self):
        return len(self._list_data)

    def set_custom_template(self, template):
        """
        Add template to a specific design option
        The template should be an instance of designtemplate class

        :param template:
        :return:
        """
        if not isinstance(template, DesignTemplate):
            print("Template should be instance of BuildSimHubAPI.measures.DesignTemplate class")
            return False
        self._custom_template.append(template)
        return True

    def set_min(self, min_val):
        if min_val < self._lower_limit:
            print("Warning: The input: " + str(min_val) + " is lower than the minimum: " +
                  str(self._lower_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        if self._unit == 'ip':
            min_val = min_val / self._unit_convert_ratio()
        self._min = min_val

    def set_max(self, max_val):
        if max_val > self._upper_limit:
            print("Warning: The input: " + str(max_val) + " is greater than the maximum: " +
                  str(self._upper_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        if self._unit == 'ip':
            max_val = max_val / self._unit_convert_ratio()
        self._max = max_val

    def set_datalist(self, data_list):
        for i in range(len(data_list)):
            data = data_list[i]
            if data < self._lower_limit:
                print("Warning: The input: " + str(data) + " is lower than the minimum: " +
                      str(self._lower_limit) + " for the measure: " + self._measure_name +
                      ". This might be rejected by the server")
            if data_list[i] > self._upper_limit:
                print("Warning: The input: " + str(data) + " is greater than the maximum: " +
                      str(self._upper_limit) + " for the measure: " + self._measure_name +
                      ". This might be rejected by the server")
            if self._unit == 'ip':
                data_list[i] = data / self._unit_convert_ratio()

        self._list_data = data_list
        return True

    def set_data(self, data):
        if data < self._lower_limit:
            print("Warning: The input: " + str(data) + " is lower than the minimum: " +
                  str(self._lower_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        if data > self._upper_limit:
            print("Warning: The input: " + str(data) + " is greater than the maximum: " +
                  str(self._upper_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        if self._unit == 'ip':
            data = data / self._unit_convert_ratio()
        self._data = data
        return True

    def get_min(self):
        if self._unit == 'ip':
            return self._min * self._unit_convert_ratio()
        return self._min

    def get_max(self):
        if self._unit == 'ip':
            return self._max * self._unit_convert_ratio()
        return self._max

    def get_datalist_string(self):
        if not self._list_data:
            if not self._default_list:
                print("Severe, no default list or data list assigned for parametric study")
                print("Error found in measure: " + self._measure_name + ". Stop processing")
                return ""
            else:
                return "[" + ",".join(str(x) for x in self._default_list) + "]"
        else:
            return "[" + ",".join(str(x) for x in self._list_data) + "]"

    def get_data_string(self):
        if self._data is None:
            print("Severe: no data assigned for applying measure: " + self._measure_name)
            print("Error: process stopped")
            return ""
        return "[" + str(self._data) + "]"

    def get_boundary_string(self):
        if self._min is None:
            print("Severe: algorithm requires user to define the minimum value - "
                  "use set_min() to define a minimum value")
            print("No minimum value found in measure: " + self._measure_name + ". Process stopped")
            return ""

        if self._max is None:
            print("Severe: algorithm requires user to define the maximum value - "
                  "use set_max() to define a maximum value")
            print("No maximum value found in measure: " + self._measure_name + ". Process stopped")
            return ""

        return "[" + str(self._min) + "," + str(self._max) + "]"

    def get_datalist(self):

        if self._unit == 'ip':
            list_data = []
            for data in self._list_data:
                data = data * self._unit_convert_ratio()
                list_data.append(data)
            return list_data
        return self._list_data

    def get_data(self):
        if self._unit == 'ip':
            data = self._data * self._unit_convert_ratio()
            return data
        return self._data

    def get_boundary(self):
        if self._min is None:
            print("Severe: algorithm requires user to define the minimum value - "
                  "use set_min() to define a minimum value")
            print("No minimum value found in measure: " + self._measure_name + ". Process stopped")
            return ()

        if self._max is None:
            print("Severe: algorithm requires user to define the maximum value - "
                  "use set_max() to define a maximum value")
            print("No maximum value found in measure: " + self._measure_name + ". Process stopped")
            return ()
        if self._unit == 'ip':
            return (self._min * self._unit_convert_ratio(), self._max * self._unit_convert_ratio())
        return (self._min, self._max)

    def get_design_template(self):
        """
        Retrieve design template from one specific design option
        The design template will be arranged as a list that contains multiple
        dict - which will eventually converted into json array contains Json objects.
        :return:
        """
        template_list = list()
        for template in self._custom_template:
            template_list.append(template.get_template())
        return template_list

#    def num_of_combinations(self):
#        comb = 0
#        for i in range(len(self._list_data)):
#            data_list = self._list_data[i]
#            if(comb == 0):
#                comb = len(data_list)
#            else:
#                comb = comb * len(data_list)
#        return comb

    def get_api_name(self):
        return self._name

    def _unit_convert_ratio(self):
        pass

    def measure_help(self):
        return self._measure_help

    @property
    def measure_name(self):
        return self._measure_name
