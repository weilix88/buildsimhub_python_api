from .model_action import ModelAction


class RoofSolarAbsorption(ModelAction):
    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'roof_absorption', unit)

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)

