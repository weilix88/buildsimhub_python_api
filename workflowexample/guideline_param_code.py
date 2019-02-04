import BuildSimHubAPI as bshapi

project_api_key = "1a920abf-ca01-4ead-9dde-dce1c629cd2c"
model_api_key = "57eb67a4-5c1e-4fbd-8c9c-74ee5b48544a"

bsh = bshapi.BuildSimHubAPIClient()

new_param = bsh.new_parametric_job(project_api_key)

measure_list = list()
wwr = bshapi.measures.WindowWallRatio()
wwr.set_datalist([0.2, 0.6])
measure_list.append(wwr)

daylit_sensor = bshapi.measures.DaylightingSensor()
daylit_template = bshapi.helpers.DesignTemplate()
daylit_template.set_class_label("Daylighting:Controls")
daylit_template.set_template_field("Lighting Control Type", "Continuous")
daylit_template.set_template_field("Minimum Input Power Fraction for Continuous Dimming Control", "0.2")
daylit_template.set_template_field("Minimum Light Output Fraction for Continuous Dimming Control", "0.3")
daylit_sensor.set_custom_template(daylit_template)
measure_list.append(daylit_sensor)

hvac = bshapi.measures.HVACTemplate()
hvac.set_datalist([1, 5, 7, 11])
measure_list.append(hvac)

# Continuous custom design
infiltration_custom_design = bshapi.measures.CustomizedMeasure('infiltration_zone', 'si')
infiltration_custom_design.add_continuous_template('ZoneInfiltration:DesignFlowRate', 'Design Flow Rate', '0.004644', '0.06266')
measure_list.append(infiltration_custom_design)

# Discrete custom design
lit_pack_design = bshapi.measures.CustomizedMeasure('lit_pack', 'si')

# we will use DiscreteMeasureOptionTemplate to assist creating a discrete design
lit_template = bshapi.measures.DiscreteMeasureOptionTemplate()
light_1_temp = dict()
light_1_temp['Watts per Zone Floor Area'] = "12.0"
lit_template.add_class_template_modify('Lights', light_1_temp)
lit_template.set_option_name('FLO')
# add the first template group to the design
lit_pack_design.add_discrete_template_options(lit_template.get_template_group())

lit_template.clear()
light_2_temp = dict()
light_2_temp['Watts per Zone Floor Area'] = "8.0"
lit_template.add_class_template_modify('Lights', light_2_temp)
lit_template.set_option_name('CFLO')
# add the second template group to the design
lit_pack_design.add_discrete_template_options(lit_template.get_template_group())

lit_template.clear()
light_3_temp = dict()
light_3_temp['Watts per Zone Floor Area'] = "6.4"
lit_template.add_class_template_modify('Lights', light_3_temp)
lit_template.set_option_name('LED')
# add the third template group to the design
lit_pack_design.add_discrete_template_options(lit_template.get_template_group())

# DONE
# now lets add this design back to the list
measure_list.append(lit_pack_design)

new_param.add_model_measures(measure_list)
param_study = new_param.submit_parametric_study(model_api_key=model_api_key, track=True)


