from .model_action import ModelAction


class HVACTemplate(ModelAction):
    # this shows the ip to si conversion rate
    # if unit is 'ip', then multiply this rate.
    # for window it is the U-value
    # convert U-value IP to SI
    # The conversion will change w/ft2 to w/m2 if ip shows
    NUM_HVAC = 14

    def __init__(self, unit="si"):
        ModelAction.__init__(self, 'hvac_template', unit)
        self._measure_name = 'HVAC'
        self._default_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        # DOAS + VRF as default
        self._data = 10
        self._lower_limit = 0
        self._upper_limit = HVACTemplate.NUM_HVAC - 1
        self._measure_help = '''
        measure name: HVAC
        Unit: not required
        Minimum: 0
        Maximum: 13
        Type: categorical
        
        This measure will change the HVAC system in the idf file
        The HVAC system types are:
        0. sys1: PTAC
        1. sys2: PTHP
        2. sys3: PSZ-AC
        3. sys4: PSZ-HP
        4. sys5: Packaged VAV with Reheat
        5. sys6: Packaged VAV with PFP Boxes
        6. sys7: VAV with Reheat
        7. sys8: VAV with PFP Boxes
        8. sys9: Warm air furnace, gas fired
        9. sys10: Warm air furnace, electric
        10. doasvrf: DOAS with variable refrigerant flow
        11. doasfancoil: DOAS with Fan coils
        12. doaswshp: DOAS with water source heat pump (ground as condenser)
        13. doascbcb: DOAS with active cool beam + convective baseboard
        14. vavfourpipebeam: VAV system with four pipe beam
        '''

    def _unit_convert_ratio(self):
        return 1.0
