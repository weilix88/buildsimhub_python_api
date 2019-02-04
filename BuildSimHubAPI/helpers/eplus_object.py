
class EnergyPlusObject(object):

    def __init__(self, class_label):
        self._object = dict()
        self._object['class_label'] = class_label
        self._values = list()

    def add_field(self, field):
        self._values.append(str(field))

    def add_field_template(self, field, value):
        self._object[field] = value

    def get_object(self):
        if self._values:
            self._object['value_array'] = self._values
        return self._object

