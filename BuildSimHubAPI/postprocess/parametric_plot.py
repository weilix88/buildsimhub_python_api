import os
try:
    import matplotlib.pyplot as plt
    from matplotlib import ticker
except ImportError:
    print('matplotlib is not installed')

try:
    import numpy as np
except ImportError:
    print('numpy is not installed')

try:
    import pandas as pd
except ImportError:
    print('pandas is not installed')


class ParametricPlot:
    def __init__(self, data, unit=""):
        self._value = data['value']
        self._unit = unit

        self._model_plot = data['model_plot']
        model_des = data['model']

        data_list = list()

        # create data dictionary
        for j in range(len(model_des)):
            col_list = model_des[j]
            parameters = col_list.split(",")
            data_dict = dict()
            for k in range(len(parameters)):
                title, val = parameters[k].split(":")
                data_dict[title.strip()] = float(val.strip())
            # data_dict['Value'] = self._value[j]

            data_list.append(data_dict)

        self._df = pd.DataFrame(data_list, index=self._model_plot)
        self._df['Value'] = self._value

    def pandas_df(self):
        return self._df

    def line_plot(self, title):
        ind = np.arange(len(self._value))
        plt.xticks(ind, self._model_plot)
        plt.plot(self._value)
        plt.ylabel(self._unit)
        plt.title(title)
        plt.show()

    def parallel_coordinate(self, title, investigate=None):
        cols = list(self._df)
        colours = list()
        hasCategory = False
        if investigate is not None and investigate in self._df.columns:
            colours = ['#2e8ad8', '#cd3785', '#c64c00', '#889a00']
            self._df[investigate] = pd.Categorical(self._df[investigate])
            colours = {self._df[investigate].cat.categories[i]: colours[i] for i, _ in enumerate(self._df[investigate].cat.categories)}
            cols.remove(investigate)
            hasCategory = True

        x = [i for i, _ in enumerate(cols)]
        fig, axes = plt.subplots(1, len(x) - 1, sharey=False, figsize=(15, 5))

        # get min, max and range for each column
        min_max_range = {}
        for col in cols:
            min_max_range[col] = [self._df[col].min(), self._df[col].max(), np.ptp(self._df[col])]
            # Normalize the data for each column
            self._df[col] = np.true_divide(self._df[col] - self._df[col].min(), np.ptp(self._df[col]))

        if not isinstance(axes, list):
            axes = [axes]
        # plot each row
        for (d, y), ax in np.ndenumerate(axes):
            for idx in self._df.index:
                if hasCategory:
                    category = self._df.loc[idx, investigate]
                    ax.plot(x, self._df.loc[idx, cols], colours[category])
                else:
                    ax.plot(x, self._df.loc[idx, cols])
            ax.set_xlim([x[y], x[y + 1]])

        # Set the tick positions and labels on y axis for each plot
        # Tick positions based on normalized data
        # Tick labels are based on original data
        def set_ticks_for_axis(dim, ax, ticks):
            min_val, max_val, val_range = min_max_range[cols[dim]]
            step = val_range / float(ticks - 1)
            tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]

            norm_min = self._df[cols[dim]].min()
            norm_range = np.ptp(self._df[cols[dim]])
            norm_step = norm_range / float(ticks - 1)
            ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
            ax.yaxis.set_ticks(ticks)
            ax.set_yticklabels(tick_labels)

        #for final axis use
        seen = set()
        last_ax = None
        total_dim = 0
        for (d, dim), ax in np.ndenumerate(axes):
            seen.clear()
            ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))

            col_data = self._df[cols[dim]]
            for i in range(len(col_data)):
                seen.add(col_data[i])

            set_ticks_for_axis(dim, ax, len(seen))
            ax.set_xticklabels([cols[dim]])
            last_ax = ax
            total_dim += 1

        # move the final axis' ticks to the right-hand side
        ax = plt.twinx(last_ax)
        # dim = len(axes)
        ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
        set_ticks_for_axis(total_dim, ax, len(seen))
        ax.set_xticklabels([cols[-2], cols[-1]])

        # Remove space between subplots
        plt.subplots_adjust(wspace=0)

        plt.title(title + " [" + self._unit + "]")

        if hasCategory:
            # add legend
            plt.legend(
                [plt.Line2D((0, 1), (0, 0), color=colours[cat]) for cat in self._df[investigate].cat.categories],
                self._df[investigate].cat.categories,
                loc=1)

        plt.show()

    def parallel_coordinate_plotly(self, investigate=None, image_name="Plot"):
        try:
            from plotly.offline import plot
            from plotly import tools
            import plotly.graph_objs as go
        except ImportError:
            print('plotly is not installed')

        cols = list(self._df)
        colours = list()
        has_category = False
        if investigate is not None and investigate in self._df.columns:
            colours = ['#2e8ad8', '#c64c00', '#cd3785', '#889a00']
            self._df[investigate] = pd.Categorical(self._df[investigate])
            colours = [[self._df[investigate].cat.categories[i], colours[i]] for i, _ in enumerate(self._df[investigate].cat.categories)]
            cols.remove(investigate)
            has_category = True

        plotly_list = list()
        for col in cols:
            #convert to cat
            seen = set()
            for val in self._df[col]:
                seen.add(val)
            data_dict = dict(range=[self._df[col].min(), self._df[col].max()], tickvals=list(seen), label=col, values=self._df[col])
            plotly_list.append(data_dict)

        data = list()
        if has_category:
            data.append(go.Parcoords(line=dict(color=self._df[investigate], colorscale=colours), dimensions=plotly_list))
        else:
            data.append(go.Parcoords(dimensions=plotly_list))

        # fig = go.Figure(data=data)
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        plot(data, filename=dir+'/' + image_name + '.html')

result_dict = {'value': [46.09, 45.6, 56.46, 56.07, 187.36, 186.94, 47.81, 47.03, 57.9, 57.25, 188.76, 188.14, 49.13, 48.12, 58.98, 58.15, 189.78, 189.0, 46.09, 45.6, 56.46, 56.07, 187.36, 186.94, 47.81, 47.03, 57.9, 57.25, 188.76, 188.14, 49.13, 48.12, 58.98, 58.15, 189.78, 189.0, 46.09, 45.6, 56.46, 56.07, 187.36, 186.94, 47.81, 47.03, 57.9, 57.25, 188.76, 188.14, 49.13, 48.12, 58.98, 58.15, 189.78, 189.0, 46.76, 46.28, 57.36, 56.96, 188.19, 187.78, 48.47, 47.7, 58.8, 58.14, 189.59, 188.97, 49.78, 48.77, 59.88, 59.06, 190.61, 189.83, 46.76, 46.28, 57.36, 56.96, 188.19, 187.78, 48.47, 47.7, 58.8, 58.14, 189.59, 188.97, 49.78, 48.77, 59.88, 59.06, 190.61, 189.83, 46.76, 46.28, 57.36, 56.96, 188.19, 187.78, 48.47, 47.7, 58.8, 58.14, 189.59, 188.97, 49.78, 48.77, 59.88, 59.06, 190.61, 189.83], 'model': ['Wall_R: 3.5, Roof_R: 4.0, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 4.0, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.5, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 3.5, Roof_R: 3.1, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 4.0, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.5, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 4.3, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 4.3, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 4.3, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 6.5, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 6.5, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 6.5, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 8.1, Infiltration: -3.0, OccupancySensor2: -3.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 8.1, Infiltration: -2.0, OccupancySensor2: -2.0, OccupancySensor: 1.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 0.0', 'Wall_R: 2.3, Roof_R: 3.1, LPD: 8.1, Infiltration: -1.0, OccupancySensor2: -1.0, OccupancySensor: 1.0'], 'model_plot': ['case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case8', 'case9', 'case10', 'case11', 'case12', 'case13', 'case14', 'case15', 'case16', 'case17', 'case18', 'case19', 'case20', 'case21', 'case22', 'case23', 'case24', 'case25', 'case26', 'case27', 'case28', 'case29', 'case30', 'case31', 'case32', 'case33', 'case34', 'case35', 'case36', 'case37', 'case38', 'case39', 'case40', 'case41', 'case42', 'case43', 'case44', 'case45', 'case46', 'case47', 'case48', 'case49', 'case50', 'case51', 'case52', 'case53', 'case54', 'case55', 'case56', 'case57', 'case58', 'case59', 'case60', 'case61', 'case62', 'case63', 'case64', 'case65', 'case66', 'case67', 'case68', 'case69', 'case70', 'case71', 'case72', 'case73', 'case74', 'case75', 'case76', 'case77', 'case78', 'case79', 'case80', 'case81', 'case82', 'case83', 'case84', 'case85', 'case86', 'case87', 'case88', 'case89', 'case90', 'case91', 'case92', 'case93', 'case94', 'case95', 'case96', 'case97', 'case98', 'case99', 'case100', 'case101', 'case102', 'case103', 'case104', 'case105', 'case106', 'case107', 'case108']}
result_unit = ""
plot = ParametricPlot(result_dict, result_unit)
plot.parallel_coordinate_plotly()
