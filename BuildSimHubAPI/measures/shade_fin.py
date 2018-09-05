from .model_action import ModelAction

'''
Measures to add fin to the model

if the model has fins, it will change the fins depth
to the specified values
if the mode has no fins, it will add fins to the left and right side of the building with the specified 
depth.

This measure applies to windows for all orientations

'''


class ShadeFin(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for ft to meter
    # The conversion will change ft to m if ip shows
    CONVERSION_RATE = 3.28084

    def __init__(self, unit="si", orientation=None):

        if orientation is None:
            ModelAction.__init__(self, 'window_fin', unit)
            self._measure_name = 'Fin'
        else:
            orientation = orientation.lower()
            if orientation == 'w':
                ModelAction.__init__(self, 'window_fin_w', unit)
                self._measure_name = 'Fin_West'
            elif orientation == 'e':
                ModelAction.__init__(self, 'window_fin_e', unit)
                self._measure_name = 'Fin_East'
            elif orientation == 's':
                ModelAction.__init__(self, 'window_fin_s', unit)
                self._measure_name = 'Fin_South'
            elif orientation == 'n':
                ModelAction.__init__(self, 'window_fin_n', unit)
                self._measure_name = 'Fin_North'
            else:
                ModelAction.__init__(self, 'window_fin', unit)
                self._measure_name = 'Fin'
        self._lower_limit = 0.1

    def _unit_convert_ratio(self):
        return ShadeFin.CONVERSION_RATE
