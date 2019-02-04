
import BuildSimHubAPI as bshapi
import pandas as pd

# project_key can be found in every project (click the information icon next to project name)
project_api_key = '921a1f04-0238-4e88-bbc5-e4eb71c352c6'
# model_key can be found in each model information bar
model_api_key = '678f3232-61ed-4347-a19c-8291b18583d7'

# initialize the client
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')


def gen_zone_sizing_object(oa_obj_name):
    """
      Sizing:Zone,
    SPACE1-1,  !- Zone or ZoneList Name
    SupplyAirTemperature,  !- Zone Cooling Design Supply Air Temperature Input Method
    14.,  !- Zone Cooling Design Supply Air Temperature {C}
    ,  !- Zone Cooling Design Supply Air Temperature Difference {deltaC}
    SupplyAirTemperature,  !- Zone Heating Design Supply Air Temperature Input Method
    43.,  !- Zone Heating Design Supply Air Temperature {C}
    ,  !- Zone Heating Design Supply Air Temperature Difference {deltaC}
    0.009,  !- Zone Cooling Design Supply Air Humidity Ratio {kgWater/kgDryAir}
    0.004,  !- Zone Heating Design Supply Air Humidity Ratio {kgWater/kgDryAir}
    SZ DSOA SPACE1-1,  !- Design Specification Outdoor Air Object Name
    0.0,  !- Zone Heating Sizing Factor
    0.0,  !- Zone Cooling Sizing Factor
    DesignDay,  !- Cooling Design Air Flow Method
    0,  !- Cooling Design Air Flow Rate {m3/s}
    .000762,  !- Cooling Minimum Air Flow per Zone Floor Area {m3/s-m2}
    0,  !- Cooling Minimum Air Flow {m3/s}
    0.2,  !- Cooling Minimum Air Flow Fraction
    DesignDay,  !- Heating Design Air Flow Method
    0,  !- Heating Design Air Flow Rate {m3/s}
    .002032,  !- Heating Maximum Air Flow per Zone Floor Area {m3/s-m2}
    .1415762,  !- Heating Maximum Air Flow {m3/s}
    0.3;  !- Heating Maximum Air Flow Fraction


    :param zone_name:
    :return:
    """
    zone_sizing_obj = bshapi.helpers.EnergyPlusObject("Sizing:Zone")
    zone_sizing_obj.add_field("zone")
    zone_sizing_obj.add_field("SupplyAirTemperature")
    zone_sizing_obj.add_field("14")
    zone_sizing_obj.add_field("")
    zone_sizing_obj.add_field("SupplyAirTemperature")
    zone_sizing_obj.add_field("43")
    zone_sizing_obj.add_field("")
    zone_sizing_obj.add_field("0.0085")
    zone_sizing_obj.add_field("0.008")
    zone_sizing_obj.add_field(oa_obj_name)
    zone_sizing_obj.add_field("1.25")
    zone_sizing_obj.add_field("1.15")
    zone_sizing_obj.add_field("DesignDay")
    zone_sizing_obj.add_field("0.0")
    zone_sizing_obj.add_field(".000762")
    zone_sizing_obj.add_field("0.0")
    zone_sizing_obj.add_field("0.2")
    zone_sizing_obj.add_field("DesignDay")
    zone_sizing_obj.add_field("0.0")
    zone_sizing_obj.add_field("0.002032")
    zone_sizing_obj.add_field("0.1415762")
    zone_sizing_obj.add_field("0.3")
    return zone_sizing_obj


def gen_ltg_sched():
    ltg_obj = bshapi.helpers.EnergyPlusObject("Schedule:Compact")
    ltg_obj.add_field("Office lighting 5 to 20")
    ltg_obj.add_field("Fraction")
    ltg_obj.add_field("Through: 12/31")
    ltg_obj.add_field("For: Weekdays SummerDesignDay")
    ltg_obj.add_field("Until: 05:00")
    ltg_obj.add_field("0.05")
    ltg_obj.add_field("Until: 07:00")
    ltg_obj.add_field("0.1")
    ltg_obj.add_field("Until: 08:00")
    ltg_obj.add_field("0.3")
    ltg_obj.add_field("Until: 17:00")
    ltg_obj.add_field("0.9")
    ltg_obj.add_field("Until: 18:00")
    ltg_obj.add_field("0.5")
    ltg_obj.add_field("Until: 20:00")
    ltg_obj.add_field("0.3")
    ltg_obj.add_field("Until: 24:00")
    ltg_obj.add_field("0.05")
    ltg_obj.add_field("For: Saturday WinterDesignDay")
    ltg_obj.add_field("Until: 06:00")
    ltg_obj.add_field("0.05")
    ltg_obj.add_field("Until: 08:00")
    ltg_obj.add_field("0.1")
    ltg_obj.add_field("Until: 12:00")
    ltg_obj.add_field("0.3")
    ltg_obj.add_field("Until: 17:00")
    ltg_obj.add_field("0.1")
    ltg_obj.add_field("Until: 24:00")
    ltg_obj.add_field("0.05")
    ltg_obj.add_field("For: AllOtherDays")
    ltg_obj.add_field("Until: 24:00")
    ltg_obj.add_field("0.05")
    return ltg_obj


# ################ Model preparation #####################

# 1. build up the zone map
# 1.1 get the seed model
model = bsh.model_results(project_api_key, model_api_key)
zone_list = model.zone_list()
zone_map = dict()

# 2. Prepare
# 2.1 add objects to model based on Zone (any object that has zone name or zone list name fields
zone_sizing_list = list()
for zone in zone_list:
    zone_sizing_list.append(zone['zone_name'])
zone_temp = gen_zone_sizing_object('OAT')
new_id = model.add_modify_zone(zone_sizing_list, [zone_temp])

# 2.2 add an object - there is data limit on this function
model = bsh.model_results(project_api_key, new_id)
new_id = model.add_object([gen_ltg_sched()])

# 2.3 add a standard HVAC system
model = bsh.model_results(project_api_key, new_id)
zone_group = dict()
for zone in zone_list:
    zone_group[zone['zone_name']] = dict()
    zone_group[zone['zone_name']]['ventilation'] = 'floor_' + str(zone['floor'])
    zone_group[zone['zone_name']]['heating'] = 'floor_' + str(zone['floor'])
    zone_group[zone['zone_name']]['cooling'] = 'floor_' + str(zone['floor'])

# new_id = model.hvac_swap(hvac_type=6, zone_group=zone_group)

# 3. Setup parameters for parametric
# param = bsh.new_parametric_job(project_api_key)

measure_list = list()
# build the parametric values

# 3.1 measures within the standard measures
wwrn = bshapi.measures.WindowWallRatio(orientation="N")
wwrn.set_min(0.3)
wwrn.set_max(0.6)
measure_list.append(wwrn)

wwrs = bshapi.measures.WindowWallRatio(orientation="S")
wwrs.set_min(0.3)
wwrs.set_max(0.6)
measure_list.append(wwrs)

# 3.2 measures with a object template
# This allows user to revise the template when applying
lpd = bshapi.measures.LightLPD()
lpd.set_min(6.8)
lpd.set_max(12.0)
light_temp = bshapi.helpers.DesignTemplate()
light_temp.set_class_label("Lights")
light_temp.set_template_field("Return Air Fraction", "0.2")
light_temp.set_template_field("Fraction Radiant", "0.6")
lpd.set_custom_template(light_temp)
measure_list.append(lpd)

# 3.3 customized measure - continuous value
# continuous variable custom measure
custom_measure = bshapi.measures.CustomizedMeasure('customized_air_infiltration', 'si')
custom_measure.add_continuous_template('ZoneInfiltration:DesignFlowRate',
                                       'Flow per Exterior Surface Area', '0.0001', '0.001')

# discrete custom measure
# discrete measure
custom_measure_2 = bshapi.measures.CustomizedMeasure('customized_thermostat', 'si')
template = bshapi.measures.DiscreteMeasureOptionTemplate()
obj_temp = dict()
obj_temp['Heating Setpoint Temperature Schedule Name'] = "HTGSETP_SCH_NO_OPTIMUM"
obj_temp['Cooling Setpoint Temperature Schedule Name'] = "CLGSETP_SCH_NO_OPTIMUM"
# template.add_class_template_modify('Lights', light_temp)
template.add_class_template_modify('ThermostatSetpoint:DualSetpoint', obj_temp, 'Working Space DualSPSched')
template.set_option_name('No_optimum_start')
custom_measure_2.add_discrete_template_options(template.get_template_group())

template.clear()

obj_temp['Heating Setpoint Temperature Schedule Name'] = "HTGSETP_SCH_OPTIMUM"
obj_temp['Cooling Setpoint Temperature Schedule Name'] = "CLGSETP_SCH_OPTIMUM"
template.add_class_template_modify('ThermostatSetpoint:DualSetpoint', obj_temp, 'Working Space DualSPSched')
template.set_option_name('Optimum_start')
custom_measure_2.add_discrete_template_options(template.get_template_group())




