import BuildSimHubAPI as bsh_api
local_file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"

# continuous custom measure
custom_measure = bsh_api.measures.CustomizedMeasure('continuous_measure', 'ip')
custom_measure.add_continuous_template('Lights', 'Lighting Level', '0.4', '1.5', 'Fun for test')

# regular measure
regular_measure = bsh_api.measures.LightLPD('ip')
regular_measure.set_min(0.6)
regular_measure.set_max(1.2)

# discrete measure
custom_measure_2 = bsh_api.measures.CustomizedMeasure('discrete_measure', 'ip')
template = bsh_api.measures.DiscreteMeasureOptionTemplate()
light_temp = dict()
light_temp['Design Level Calculation Method'] = "LightingLevel"
light_temp['Lighting Level'] = "1000"
# template.add_class_template_modify('Lights', light_temp)
template.add_class_template_modify('Lights', light_temp, 'SPACE1-1 Lights 1')
template.set_option_name('Flo')
custom_measure_2.add_discrete_template_options(template.get_template_group())

template.clear()

light_temp['Design Level Calculation Method'] = "LightingLevel"
light_temp['Lighting Level'] = "600"
# template.add_class_template_modify('Lights', light_temp)
template.add_class_template_modify('Lights', light_temp, 'SPACE1-1 Lights 1')
template.set_option_name('LED')
custom_measure_2.add_discrete_template_options(template.get_template_group())

template.clear()
template.add_class_template_delete('Lights', 'SPACE2-1 Lights 2')
template.set_option_name('NoSPACE2Lit')
custom_measure_2.add_discrete_template_options(template.get_template_group())

bsh = bsh_api.BuildSimHubAPIClient()
param = bsh.new_parametric_job('f98aadb3-254f-428d-a321-82a6e4b9424c')
# param.add_model_measure(custom_measure)
param.add_model_measure(custom_measure_2)
param.add_model_measure(regular_measure)

param.submit_parametric_study_local(local_file_dir, algorithm='montecarlo', size=4,
                                                   track=True)
