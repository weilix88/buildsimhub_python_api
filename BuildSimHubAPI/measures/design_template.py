
class DesignTemplate(object):
    def __init__(self):
        self._template_dict = dict()

    def set_class_label(self, label):
        """
        Set the class label.
        E.g. BuildingSurface:Detailed
        :param label:
        :return:
        """
        self._template_dict['class_label'] = label

    def set_template_field(self, field_name, value):
        """
        Set the field name.
        E.g. Lighting Power Density
        :param field_name:
        :param value:
        :return:
        """
        self._template_dict[field_name] = value

    def set_class_name(self, name):
        """
        Set the class name
        :param name:
        :return:
        """
        self._template_dict['class_name'] = name

    def get_template(self):
        return self._template_dict
