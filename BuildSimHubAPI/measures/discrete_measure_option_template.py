"""
This is a helper class that helps user to create discrete measure templates
for parametric studies.
"""


class DiscreteMeasureOptionTemplate(object):
    def __init__(self):
        self._template_group = list()
        self._option_name = 'default'

    def set_option_name(self, name):
        self._option_name = name

    def add_class_template_modify(self, class_label, template, class_name=None):
        """
        Add the template for an EnergyPlus class and do modification operation

        Modification operation means this template modifies existing classes that matches
        class_label (e.g. Lights) or matches class_label (e.g. Lights) and class_name (SPACE1-1 Lights)
        according to the template

        Template should be a dict and arranged in a field_name: value format e.g.
        equip['Design Level Calculation Method'] = 'EquipmentLevel'
        equip['Design Level'] = '120'

        measure_template.add_class_template_modify('ElectricEquipment', equip)

        :param class_label: EnergyPlus class label, e.g. Lights in str
        :param template: class template, must be a dict
        :param class_name: the class name, e.g. SPACE1-1 Lights (optional)
        :return: True if success, False otherwise
        """

        # TODO check template is dict or not

        template['operation'] = 'modify'
        template['class_label'] = class_label
        if class_name is not None:
            template['class_name'] = class_name

        self._template_group.append(template)
        return True

    def add_class_template_delete(self, class_label, class_name=None):
        """
        Add the template for an EnergyPlus class and do delete operation

        delete operation means this template removes existing classes that matches
        class_label (e.g. Lights) or matches class_label (e.g. Lights) and class_name (SPACE1-1 Lights)

        measure_template.add_class_template_delete('ElectricEquipment', 'PLENUM1 Electric')
        This will deletes the EnergyPlus class: ElectricEquipment with the name of PLENUM1 Electric

        :param class_label: EnergyPlus class label, e.g. ElectricEquipment
        :param class_name: The class name, e.g. SPACE1-1 Lights
        :return: True if added, False otherwise
        """

        # TODO check template is dict or not

        delete_temp = dict()
        delete_temp['operation'] = 'delete'
        delete_temp['class_label'] = class_label
        if class_name is not None:
            delete_temp['class_name'] = class_name

        self._template_group.append(delete_temp)
        return True

    def clear(self):
        """
        Clear all the templates in the group
        :return:
        """
        self._option_name = 'default'
        self._template_group.clear()

    def get_template_group(self):
        option_temp = dict()
        option_temp['option_name'] = self._option_name

        option_list = list()
        for temp in self._template_group:
            option_list.append(temp)
        option_temp['template_group'] = option_list

        return option_temp

