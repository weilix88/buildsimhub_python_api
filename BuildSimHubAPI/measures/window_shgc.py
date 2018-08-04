from .model_action import ModelAction


class WindowSHGC(ModelAction):

    def __init__(self, orientation=None):
        if orientation is None:
            ModelAction.__init__(self, 'window_shgc')
        else:
            orientation = orientation.lower()
            if orientation == 'w':
                ModelAction.__init__(self, 'window_shgc_w')
            elif orientation == 'e':
                ModelAction.__init__(self, 'window_shgc_e')
            elif orientation == 's':
                ModelAction.__init__(self, 'window_shgc_s')
            elif orientation == 'n':
                ModelAction.__init__(self, 'window_shgc_n')
            else:
                ModelAction.__init__(self, 'window_shgc')

    def get_num_value(self):
        return ModelAction.num_of_value(self)

    def set_datalist(self, datalist):
        ModelAction.set_datalist(self, datalist)
