"""
This post-process class shows the integration of parametric results with plotly.
Plotly is an open-source project that can be found in: https://plot.ly

It is required to have the latest plotly python package in your python.

"""
import os

try:
    import pandas as pd
except ImportError:
    pd = None
    print('pandas is not installed')


class ParametricPlot(object):

    def __init__(self, data, unit=""):
        """
        Construct parametric plot

        :param data: returned from the parametric result call
        :param unit:
        """
        self._value = data['value']
        self._unit = unit

        self._model_plot = data['model_plot']
        self._model_des = data['model']

        data_list = list()

        # create data dictionary
        for j in range(len(self._model_des)):
            col_list = self._model_des[j]
            parameters = col_list.split(",")
            data_dict = dict()
            for k in range(len(parameters)):
                title, val = parameters[k].split(":")
                # for cases like on off options
                if val.strip() == 'Off':
                    val = '0'
                if val.strip() == 'On':
                    val = '1'

                data_dict[title.strip()] = float(val.strip())
            # data_dict['Value'] = self._value[j]

            data_list.append(data_dict)

        self._df = pd.DataFrame(data_list, index=self._model_plot)
        self._df['Value'] = self._value

    def pandas_df(self):
        """get the data in pandas dataframe"""
        return self._df

    def scatter_chart_plot(self, title='line graph plot', image_name='line'):
        """Plotly scatter plot"""
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')

        data = list()
        trace = go.Scatter(
            x=self._model_plot,
            y=self._value,
            mode='markers',
            marker=dict(size=14,
                        line=dict(width=1)),
            text=self._model_des
        )
        data.append(trace)

        layout = go.Layout(
            title=title,
            xaxis=dict(
                title='Parametric cases',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title=self._unit,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )

        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        fig = dict(data=data, layout=layout)
        plot(fig, filename=dir + '/' + image_name + '.html')

    def parallel_coordinate_plot(self, investigate=None, image_name="Plot"):
        """
        Plotly parallel coordinate plot

        :param investigate: parameter in the legend
        :param image_name: name of the image
        :return:
        """
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')

        cols = list(self._df)
        has_category = False
        if investigate is not None and investigate in self._df.columns:
            cols.remove(investigate)
            has_category = True

        plotly_list = list()
        for col in cols:
            data_dict = dict(range=[self._df[col].min(), self._df[col].max()],
                             label=col, values=self._df[col], tickformat='.2f')
            plotly_list.append(data_dict)

        data = list()
        if has_category:
            data.append(go.Parcoords(line=dict(color=self._df[investigate], colorscale='Viridis',
                                               showscale=True, colorbar=dict(title=investigate)), dimensions=plotly_list))
        else:
            data.append(go.Parcoords(dimensions=plotly_list))

        # fig = go.Figure(data=data)
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        plot(data, filename=dir + '/' + image_name + '.html')
