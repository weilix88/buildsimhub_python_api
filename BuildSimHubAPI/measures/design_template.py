
class DesignTemplate(object):
    def __init__(self):
        self._class_label = ""
        self._field_name = ""
        self._value = ""
        self._class_name = ""

    def set_class_label(self, label):
        """
        Set the class label.
        E.g. BuildingSurface:Detailed
        :param label:
        :return:
        """
        self._class_label = label

    def set_field_name(self, field):
        """
        Set the field name.
        E.g. Lighting Power Density
        :param field:
        :return:
        """
        self._field_name = field

    def set_class_name(self, name):
        """
        Set the class name
        :param name:
        :return:
        """
        self._class_name = name

    def set_value(self, value):
        """
        Set the value
        :param value:
        :return:
        """
        self._value = value

    def get_template(self):
        template = dict()
        template['class_label'] = self._class_label
        template['field_name'] = self._field_name
        template['class_name'] = self._class_name
        template['value'] = self._value
        return template
