"""
The example demonstrates how to use plotly dash for creating a dashboard from the parametric simulations generated
in the BuildSim cloud.
"""

import BuildSimHubAPI as bshapi
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sklearn import linear_model

# USER INPUTS
# model_key can be found in each model information bar
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
model_api_key = "9ad4b655-db49-4451-9b63-82470df3cae8"

# initialization
# Get model list and results
bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
app = dash.Dash()
budget = 150000
measure_list = list()


def window_wall_ratio_cost(val):
    return -13143.2 * val + 33255.32


def wall_r_cost(val):
    return 432 * val + 11230.2


def lpd_cost(val):
    return -8112 * val + 19885.4


def chiller_cost(val):
    return 8732.2 * val + 23222.22


def boiler_cost(val):
    return 9174.44 * val + 17837.99


# constraint function
def cost(x_pred):
    cost = 0.0
    for i in range(len(column_head)):
        head = column_head[i].strip()
        if head == 'Wall_R':
            cost += wall_r_cost(x_pred[i])
        elif head == 'LPD':
            cost += lpd_cost(x_pred[i])
        elif head == 'ChillerCOP':
            cost += chiller_cost(x_pred[i])
        elif head == 'HeatingEff':
            cost += boiler_cost(x_pred[i])
        else:
            cost += window_wall_ratio_cost(x_pred[i])
    return cost


def convert_parajson_pandas(result_dict):
    for i in range(len(result_dict)):
        tempstr = result_dict["value"]

    dict = {}
    for key in result_dict:
        if key == "model":
            templist = result_dict[key]
            tempdict = {}
            for i in range(len(templist)):
                tempstr = result_dict["model"][i]
                templist = tempstr.split(',')
                for j in range(len(templist)):
                    pair = templist[j].split(': ')
                    if pair[0] not in tempdict:
                        tempdict[pair[0]] = []
                    tempdict[pair[0]].append(pair[1])
            for subkey in tempdict:
                dict[subkey] = tempdict[subkey]
        elif key != 'model_plot':
            dict[key] = result_dict[key]
    return pd.DataFrame(dict)


def generate_parametric_dict(models):
    temp_dict = {}
    for model in models:
        commit_msg = model['commit_msg']
        commit_id = model['commit_id']

        measure_info_array = commit_msg.split(',')
        for i in range(len(measure_info_array)):
            key_value_list = measure_info_array[i].split(':')
            if len(key_value_list) != 2:
                continue
            if key_value_list[0] not in temp_dict:
                temp_dict[key_value_list[0]] = []
            temp_dict[key_value_list[0]].append(key_value_list[1].strip())

        if 'commit_id' not in temp_dict:
            temp_dict['commit_id'] = []
        temp_dict['commit_id'].append(commit_id)

    return temp_dict


def parallel_coordinate(dictionary):
    color_list = []
    for i in dictionary:
        number_of_rows = len(dictionary[i])
        for j in range(number_of_rows):
            color_list.append((-1) * j)
        break

    dimensions = list()
    for key in dictionary:
        if key != 'commit_id':
            temp = dict()
            temp['range'] = [min(dictionary[key]), max(dictionary[key])]
            temp['label'] = key
            temp['values'] = dictionary[key]
            temp['tickformat'] = '0.2f'
            dimensions.append(temp)

    data3 = [
        go.Parcoords(
            line=dict(
                color=color_list,
                colorscale='Jet',
                showscale=True,
                reversescale=True,
                cmin=-200,  # value =200k
                cmax=0),
            dimensions=dimensions
        )
    ]

    fig3 = go.Figure(data=data3)
    return fig3


model_list = bsh.model_list(project_api_key, model_api_key)
model_dict = generate_parametric_dict(model_list)

# The measures:
# Define EEMs
wwrn = bshapi.measures.WindowWallRatio(orientation="N")
wwrn.set_min(0.3)
wwrn.set_max(0.6)
measure_list.append(wwrn)

wwrs = bshapi.measures.WindowWallRatio(orientation="S")
wwrs.set_min(0.3)
wwrs.set_max(0.6)
measure_list.append(wwrs)

wwrw = bshapi.measures.WindowWallRatio(orientation="W")
wwrw.set_min(0.3)
wwrw.set_max(0.6)
measure_list.append(wwrw)

wwre = bshapi.measures.WindowWallRatio(orientation="E")
wwre.set_min(0.3)
wwre.set_max(0.6)
measure_list.append(wwre)

wallr = bshapi.measures.WallRValue('ip')
wallr.set_min(20)
wallr.set_max(40)
measure_list.append(wallr)

lpd = bshapi.measures.LightLPD('ip')
lpd.set_min(0.6)
lpd.set_max(1.2)
measure_list.append(lpd)

chillerEff = bshapi.measures.CoolingChillerCOP()
chillerEff.set_min(3.5)
chillerEff.set_max(5.5)
measure_list.append(chillerEff)

heatEff = bshapi.measures.HeatingEfficiency()
heatEff.set_min(0.8)
heatEff.set_max(0.95)
measure_list.append(heatEff)

# Get parametric result objects
model_results = bsh.parametric_results(project_api_key, model_api_key)
eui = model_results.net_site_eui()

# Train a model
df = convert_parajson_pandas(eui)
y = df.loc[:, 'value']
x = df.loc[:, df.columns != 'value']
column_head = list(x)
# train a regression model
alg = linear_model.LinearRegression()
alg.fit(x, y)


def fun(x_pred): return alg.predict([x_pred])


# we will retrieve end use data of each models
#min_electricity_model = bsh.model_results(project_api_key, electric_min_id)
#min_naturalgas_model = bsh.model_results(project_api_key, naturalgas_min_id)
#min_total_model = bsh.model_results(project_api_key, total_min_id)

#end_use_array = list()
#end_use_array.append(min_electricity_model.html_table('Annual Building Utility Performance Summary',
#                                                          'End Uses'))
#end_use_array.append(min_naturalgas_model.html_table('Annual Building Utility Performance Summary',
#                                                         'End Uses'))
#end_use_array.append(min_total_model.html_table('Annual Building Utility Performance Summary',
#                                                    'End Uses'))
#bar = bar_chart(end_use_array, model_label_list)
#map = polar_map(end_use_array, model_label_list)
parallel = parallel_coordinate(model_dict)

app.layout = html.Div(children=[
    html.Div(
        [
            dcc.Markdown(
                """
                ## Buildsim Plot.ly Dashboard
                ***
                """.replace('  ', ''),
                className='eight columns offset-by-two'
            )
        ],
        className='row',
        style=dict(textAlign="center", marginBottom="15px")
    ),

    # GRAPHS:
    #html.Div([
    #    html.H5('Bar Chart', style=dict(textAlign="center")),
    #    dcc.Graph(id='bar', figure=bar)]
    #),

    #html.Div([
    #    html.H5('Polar Map', style=dict(textAlign="center")),
    #    dcc.Graph(id='map', figure=map)]
    #),

    html.Div([
        html.H5('Parallel Coordinate', style=dict(textAlign="center")),
        dcc.Graph(id='parallel', figure=parallel)]
    ),

    html.Div(
        html.Hr(className='eight columns offset-by-two'),
        className="row"
    ),

    # Value Display
    html.Div(children=[
        html.Div([
            html.H3(id='eui_predicted', style=dict(textAlign="center")),
        ]),
        html.Div([
            html.H3(id='cost_predicted', style=dict(textAlign="center")),
        ])
    ], style={'columnCount': 2, 'marginBottom': '15px',
              'marginRight': '100px', 'marginLeft': '100px'}),

    html.Div(
        html.Hr(className='eight columns offset-by-two'),
        className="row"
    ),

    #ML FIELD
    html.Div(children=[
        html.Div(children=[
            html.Div(id='lpd_power'),
            dcc.Slider(
                id='lpd_slider',
                min=0.6,
                max=1.2,
                step=0.1,
                value=0.8
            )
        ]),

        html.Div(children=[
            html.Div(id='wall_r_value'),
            dcc.Slider(
                id='wall_r_slider',
                min=20,
                max=40,
                step=1.0,
                value=25
            )
        ]),

        html.Div(children=[
            html.Div(id='wwr_s'),
            dcc.Slider(
                id='win_wall_r_south',
                min=0.3,
                max=0.6,
                step=0.05,
                value=0.4
            )
        ]),

        html.Div(children=[
            html.Div(id='wwr_n'),
            dcc.Slider(
                id='win_wall_r_north',
                min=0.3,
                max=0.6,
                step=0.05,
                value=0.4
            )
        ]),

        html.Div(children=[
            html.Div(id='wwr_e'),
            dcc.Slider(
                id='win_wall_r_east',
                min=0.3,
                max=0.6,
                step=0.05,
                value=0.4
            )
        ]),

        html.Div(children=[
            html.Div(id='wwr_w'),
            dcc.Slider(
                id='win_wall_r_west',
                min=0.3,
                max=0.6,
                step=0.05,
                value=0.4
            )
        ]),

        html.Div(children=[
            html.Div(id='chiller_cop'),
            dcc.Slider(
                id='chiller_cop_slider',
                min=3.5,
                max=5.5,
                step=0.1,
                value=4.0
            )
        ]),

        html.Div(children=[
            html.Div(id='heating_eff'),
            dcc.Slider(
                id='heating_eff_slider',
                min=0.8,
                max=0.95,
                step=0.01,
                value=0.9
            )
        ])
    ], className='row',
       style={'columnCount': 2, 'textAlign': "center", 'marginBottom': '15px',
              'marginRight': '100px', 'marginLeft': '100px'}
    ),

    html.Div(
        html.Hr(className='eight columns offset-by-two'),
        className="row"
    ),

    html.Div([
        html.Button('Generate Model', id='download_model'),
        html.Div(id='output-container-button',
                 children='Enter a value and press submit')
    ], style={'textAlign': "center", 'marginBottom': '15px',
              'marginRight': '100px', 'marginLeft': '100px'})
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    dash.dependencies.Output('eui_predicted', 'children'),
    [dash.dependencies.Input('wall_r_slider', 'value'),
        dash.dependencies.Input('lpd_slider', 'value'),
        dash.dependencies.Input('chiller_cop_slider', 'value'),
        dash.dependencies.Input('heating_eff_slider', 'value'),
        dash.dependencies.Input('win_wall_r_south', 'value'),
        dash.dependencies.Input('win_wall_r_west', 'value'),
        dash.dependencies.Input('win_wall_r_east', 'value'),
        dash.dependencies.Input('win_wall_r_north', 'value')
     ])
def update_eui(wall, lpd, chiller, heating, wwrs, wwrw, wwre, wwrn):
    x = [wall, lpd, chiller, heating, wwrs, wwrw, wwre, wwrn]
    eui = fun(x)[0]
    return 'EUI (kBtu/ft2): {}'.format(eui)


@app.callback(
    dash.dependencies.Output('cost_predicted', 'children'),
    [dash.dependencies.Input('wall_r_slider', 'value'),
        dash.dependencies.Input('lpd_slider', 'value'),
        dash.dependencies.Input('chiller_cop_slider', 'value'),
        dash.dependencies.Input('heating_eff_slider', 'value'),
        dash.dependencies.Input('win_wall_r_south', 'value'),
        dash.dependencies.Input('win_wall_r_west', 'value'),
        dash.dependencies.Input('win_wall_r_east', 'value'),
        dash.dependencies.Input('win_wall_r_north', 'value')
     ])
def update_cost(wall, lpd, chiller, heating, wwrs, wwrw, wwre, wwrn):
    x = [wall, lpd, chiller, heating, wwrs, wwrw, wwre, wwrn]
    cost_val = cost(x)
    return 'Total Cost ($): {}'.format(cost_val)


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('download_model', 'n_clicks')],
    [dash.dependencies.State('wall_r_slider', 'value'),
     dash.dependencies.State('lpd_slider', 'value'),
     dash.dependencies.State('chiller_cop_slider', 'value'),
     dash.dependencies.State('heating_eff_slider', 'value'),
     dash.dependencies.State('win_wall_r_south', 'value'),
     dash.dependencies.State('win_wall_r_west', 'value'),
     dash.dependencies.State('win_wall_r_east', 'value'),
     dash.dependencies.State('win_wall_r_north', 'value')
     ])
def update_button(n_clicks, wall_val, lpd_val, chiller_val, heating_val, wwrs_val, wwrw_val, wwre_val, wwrn_val):
    new_measure_list = list()
    wallr.set_data(wall_val)
    new_measure_list.append(wallr)
    lpd.set_data(lpd_val)
    new_measure_list.append(lpd)
    chillerEff.set_data(chiller_val)
    new_measure_list.append(chillerEff)
    heatEff.set_data(heating_val)
    new_measure_list.append(heatEff)
    wwrs.set_data(wwrs_val)
    new_measure_list.append(wwrs)
    wwre.set_data(wwre_val)
    new_measure_list.append(wwre)
    wwrn.set_data(wwrn_val)
    new_measure_list.append(wwrn)
    wwrw.set_data(wwrw_val)
    new_measure_list.append(wwrw)

    model = bsh.model_results(project_api_key, model_api_key)
    new_api_key = model.model_copy(project_api_key)

    new_model = bsh.model_results(project_api_key, new_api_key)
    updated_model_key = new_model.apply_measures(new_measure_list)
    updated_model = bsh.model_results(project_api_key, updated_model_key)

    url = updated_model.bldg_geo(False)

    link = html.Div(
        children=[
            html.P('Generation Successfully! View model:'),
            html.A('Link', href=url)
        ]
    )

    return link


@app.callback(
    dash.dependencies.Output('heating_eff', 'children'),
    [dash.dependencies.Input('heating_eff_slider', 'value')])
def update_output(value):
    return 'Heating Efficiency: {}'.format(value)


@app.callback(
    dash.dependencies.Output('chiller_cop', 'children'),
    [dash.dependencies.Input('chiller_cop_slider', 'value')])
def update_output(value):
    return 'Chiller COP: {}'.format(value)


@app.callback(
    dash.dependencies.Output('wwr_s', 'children'),
    [dash.dependencies.Input('win_wall_r_south', 'value')])
def update_output(value):
    return 'Window Wall Ratio South: {}'.format(value)


@app.callback(
    dash.dependencies.Output('wwr_n', 'children'),
    [dash.dependencies.Input('win_wall_r_north', 'value')])
def update_output(value):
    return 'Window Wall Ratio North: {}'.format(value)


@app.callback(
    dash.dependencies.Output('wwr_e', 'children'),
    [dash.dependencies.Input('win_wall_r_east', 'value')])
def update_output(value):
    return 'Window Wall Ratio East: {}'.format(value)


@app.callback(
    dash.dependencies.Output('wwr_w', 'children'),
    [dash.dependencies.Input('win_wall_r_west', 'value')])
def update_wwrw(value):
    return 'Window Wall Ratio West: {}'.format(value)


@app.callback(
    dash.dependencies.Output('lpd_power', 'children'),
    [dash.dependencies.Input('lpd_slider', 'value')])
def update_lpd(value):
    return 'LPD (W/ft2): {}'.format(value)


@app.callback(
    dash.dependencies.Output('wall_r_value', 'children'),
    [dash.dependencies.Input('wall_r_slider', 'value')])
def update_wall_r(value):
    return 'Wall_R value: {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
