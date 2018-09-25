from .model_action import ModelAction


class CustomizedMeasure(ModelAction):
    def __init__(self, measure_name, unit='si'):
        ModelAction.__init__(self, 'user_defined', unit)
        self._measure_name = measure_name
        self._discrete_options = list()
        self._continuous_template = dict()

    def add_continuous_template(self, class_label, field_name, minimum, maximum, class_name=None):
        self._continuous_template['class_label'] = class_label
        self._continuous_template['field_name'] = field_name
        self._continuous_template['values'] = [float(minimum), float(maximum)]
        if class_name is not None:
            self._continuous_template['class_name'] = class_name

    def add_discrete_template_options(self, template):
        """
        This adds the options to the discrete values as template
        :param template:
        :return:
        """
        self._list_data.append(len(self._discrete_options))
        self._discrete_options.append(template)

    def get_data_type(self):
        if len(self._discrete_options) > 0:
            # there is discrete options in the measure - set to categorical data
            return 1
        else:
            return 0

    def get_datalist_string(self):
        data_type = self.get_data_type()
        if data_type == 0:
            self._continuous_template['measure_name'] = self._measure_name
            self._continuous_template['data_type'] = data_type
            self._continuous_template['unit'] = self._unit
            return self._continuous_template
        elif data_type == 1:
            temp_discrete = dict()
            temp_discrete['measure_name'] = self._measure_name
            temp_discrete['data_type'] = data_type
            temp_discrete['unit'] = self._unit

            value_list = list()
            for i in range(len(self._discrete_options)):
                value_list.append(i)
            temp_discrete['values'] = value_list
            temp_discrete['options'] = self._discrete_options
            return temp_discrete

    def get_boundary_string(self):
        return self.get_datalist_string()

