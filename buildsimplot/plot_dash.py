"""
The example demonstrates how to use plotly dash for creating a dashboard from the parametric simulations generated
in the BuildSim cloud.
"""

import BuildSimHubAPI as bshapi
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html

# initialization
app = dash.Dash()


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


def map_results(parametric_dict, result, key):
    parametric_dict[key] = result['value']


def sum_value(start, end, search_value, lst):
    res = []
    for i in range(start, end+1):
        # print(lst[i]['data']['array'][0]['row'])
        temp_num = 0.0
        for j in range(len(lst[i]['data']['array'])):
            if lst[i]['data']['array'][j]['row'] == search_value and float(lst[i]['data']['array'][j]['value']) != 0.0:
                temp_num = temp_num + float(lst[i]['data']['array'][j]['value'])
        res.append(temp_num)
    return res


def bar_chart(lst, model_label_list):
    data_dict = dict()

    for i in range(len(lst)):
        data = lst[i]['data']['array']
        for cell in data:
            row = cell['row']
            if row != '\xa0' and row != 'Total End Uses':
                if row not in data_dict:
                    data_dict[row] = [0, 0, 0]
                data_dict[row][i] += float(cell['value'])

    data1 = []
    for key in data_dict:
        if sum(data_dict[key]) > 0:
            trace = go.Bar(
                x=model_label_list,
                y=data_dict[key],
                name=key
            )
            data1.append(trace)

    layout1 = go.Layout(
        barmode='stack'
    )

    fig1 = go.Figure(data=data1, layout=layout1)
    return fig1


def polar_map(lst, model_label_list):
    data2 = list()

    for i in range(len(lst)):
        data = lst[i]['data']['array']
        data_dict = dict()
        for cell in data:
            row = cell['row']
            if row != '\xa0' and row != 'Total End Uses':
                if row not in data_dict:
                    data_dict[row] = 0
                data_dict[row] += float(cell['value'])
        # now we need to reorganize
        r = list()
        theta = list()
        for key in data_dict:
            if data_dict[key] > 0:
                r.append(data_dict[key])
                theta.append(key)
        data2.append(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            name=model_label_list[i]
        ))

    layout2 = go.Layout(
        polar=dict(
            domain=dict(
                x=[50, 0.46],
                y=[80, 100]
            ),
            radialaxis=dict(
                angle=45
            ),
            angularaxis=dict(
                direction="clockwise",
                period=6
            )
        )
    )

    fig2 = go.Figure(data=data2, layout=layout2)
    return fig2


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


def main():
    # model_key can be found in each model information bar
    # paste your project api key
    project_api_key = '6e764740-cb49-40ed-8a1a-1331b1d87ed2'
    # paste your model api key
    model_api_key = "8153a89b-e98a-4be1-9600-a28282b822bd"

    # Get model list and results
    bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

    model_list = bsh.model_list(project_api_key, model_api_key)
    model_dict = generate_parametric_dict(model_list)

    # Get parametric result objects
    model_results = bsh.parametric_results(project_api_key, model_api_key)
    electricity = model_results.total_end_use_electricity()
    naturalgas = model_results.total_end_use_naturalgas()

    # insert results into a dictionary
    map_results(model_dict, electricity, 'Electricity')
    map_results(model_dict, naturalgas, 'NaturalGas')

    # define the selection of a few data -
    model_label_list = ['Min Electricity', 'Min NaturalGas', 'Min Total']
    # min electricity model
    electric_min_id = 0
    electric_min = float('inf')
    # min natural gas model
    naturalgas_min_id = 0
    naturalgas_min = float('inf')
    # min total model
    total_min_id = 0
    total_min = float('inf')

    electricity_array = model_dict['Electricity']
    naturalgas_array = model_dict['NaturalGas']
    commit_id_array = model_dict['commit_id']

    for i in range(len(electricity_array)):
        if electricity_array[i] < electric_min:
            electric_min = electricity_array[i]
            electric_min_id = commit_id_array[i]

        if naturalgas_array[i] < naturalgas_min:
            naturalgas_min = naturalgas_array[i]
            naturalgas_min_id = commit_id_array[i]

        if electricity_array[i] + naturalgas_array[i] < total_min:
            total_min = electricity_array[i] + naturalgas_array[i]
            total_min_id = commit_id_array[i]

    # we will retrieve end use data of each models
    min_electricity_model = bsh.model_results(project_api_key, electric_min_id)
    min_naturalgas_model = bsh.model_results(project_api_key, naturalgas_min_id)
    min_total_model = bsh.model_results(project_api_key, total_min_id)

    end_use_array = list()
    end_use_array.append(min_electricity_model.html_table('Annual Building Utility Performance Summary',
                                                          'End Uses'))
    end_use_array.append(min_naturalgas_model.html_table('Annual Building Utility Performance Summary',
                                                         'End Uses'))
    end_use_array.append(min_total_model.html_table('Annual Building Utility Performance Summary',
                                                    'End Uses'))
    bar = bar_chart(end_use_array, model_label_list)
    map = polar_map(end_use_array, model_label_list)
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

        html.Div([
            html.H5('Bar Chart', style=dict(textAlign="center")),
            dcc.Graph(id='bar', figure=bar)]
        ),

        html.Div([
            html.H5('Polar Map', style=dict(textAlign="center")),
            dcc.Graph(id='map', figure=map)]
        ),

        html.Div([
            html.H5('Parallel Coordinate', style=dict(textAlign="center")),
            dcc.Graph(id='parallel', figure=parallel)]
        )

    ])

    app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })


main()

if __name__ == '__main__':
    app.run_server(debug=True)
