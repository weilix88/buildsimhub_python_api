from .model_action import ModelAction

'''
Measures to add overhangs to the model

if the model has overhang, it will change the overhangs depth
to the specified values
if the mode has no overhang, it will add overhang with the specified 
depth.
if the model has overhang, but overhang depth is set to 0, it will 

This measure applies to windows for all orientations

'''


class ShadeOverhang(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for ft to meter
    # The conversion will change ft to m if ip shows
    CONVERSION_RATE = 3.28084

    def __init__(self, unit="si", orientation=None):

        if orientation is None:
            ModelAction.__init__(self, 'window_overhang', unit)
            self._measure_name = 'Overhang'
        else:
            orientation = orientation.lower()
            if orientation == 'w':
                ModelAction.__init__(self, 'window_overhang_w', unit)
                self._measure_name = 'Overhang_West'
            elif orientation == 'e':
                ModelAction.__init__(self, 'window_overhang_e', unit)
                self._measure_name = 'Overhang_East'
            elif orientation == 's':
                ModelAction.__init__(self, 'window_overhang_s', unit)
                self._measure_name = 'Overhang_South'
            elif orientation == 'n':
                ModelAction.__init__(self, 'window_overhang_n', unit)
                self._measure_name = 'Overhang_North'
            else:
                ModelAction.__init__(self, 'window_overhang', unit)
                self._measure_name = 'Overhang'
            self._lower_limit = 0.0
        self._measure_help = '''
            measure name: Overhang_[Orientation]
            Unit: ip or si
            Minimum: 0
            Maximum: NA
            Type: numeric

            This measure will add Overhangs to the building or a specific orientation
            If the value is 0, then it will remove the fins
            or if the value is larger than 0, it will adds overhang with depth equal to the value
            '''

    def _unit_convert_ratio(self):
        return ShadeOverhang.CONVERSION_RATE
