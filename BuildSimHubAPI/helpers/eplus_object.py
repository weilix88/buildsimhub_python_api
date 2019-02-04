
class EnergyPlusObject(object):

    def __init__(self, class_label):
        self._object = dict()
        self._object['class_label'] = class_label
        self._values = list()
        self._comment = list()

    def add_field(self, field, comment=None):
        self._values.append(str(field))
        if comment is None:
            self._comment.append("")
        else:
            self._comment.append(comment)

    def get_object(self):
        self._object['value_array'] = self._values
        self._object['comment_array'] = self._comment
        return self._object

