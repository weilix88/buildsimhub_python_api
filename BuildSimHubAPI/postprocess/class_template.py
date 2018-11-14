class ClassTemplate(object):
    def __init__(self, temp_data):
        self._num_fields = 0
        self._field_data = []
        for data in temp_data:
            self._field_data.append(FieldTemplate(data))
            self._num_fields += 1

    def get_field(self, index=0):
        return self._field_data[index]


class FieldTemplate(object):
    def __init__(self, field_data):
        self._field_name = ''
        self._field_type = ''

        if 'field_name' in field_data:
            self._field_name = field_data['field_name']

        if 'field_type' in field_data:
            self._field_type = field_data['field_type']

        if 'field_link' in field_data:
            self._field_link = field_data['field_link']

        if 'field_key' in field_data:
            self._field_key = field_data['field_key']

        if 'max' in field_data:
            self._max = field_data['max']

        if 'min' in field_data:
            self._min = field_data['min']

        if 'unit' in field_data:
            self._unit = field_data['unit']

    @property
    def field_name(self):
        return self._field_name

    @property
    def field_type(self):
        return self._field_type

    @property
    def field_link(self):
        return self._field_link

    @property
    def field_key(self):
        return self._field_key

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def unit(self):
        return self._unit
