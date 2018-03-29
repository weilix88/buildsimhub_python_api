from .model_action import ModelAction


# this class applies overall wwr - no orientation specified


class WindowWallRatio(ModelAction):

    def __init__(self):
        ModelAction.__init__(self, 'window_wall_ratio')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_data(self, data):
        if data > 1.0 or data < 0.0:
            return False
        else:
            ModelAction.set_data(data)

    def set_datalist(self, data_list):
        for d in data_list:
            if d > 1.0 or d < 0.0:
                return False
        ModelAction.set_datalist(self, data_list)
