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
        init_index = 0
        for j in range(len(model_des)):
            col_list = model_des[j]
            if col_list == 'INIT':
                init_index = j
                continue
            parameters = col_list.split(",")
            data_dict = dict()
            for k in range(len(parameters)):
                title, val = parameters[k].split(":")
                data_dict[title.strip()] = float(val.strip())
            # data_dict['Value'] = self._value[j]

            data_list.append(data_dict)

        self._model_plot.pop(init_index)
        self._value.pop(init_index)
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

#result_dict = {'value': [29.34, 29.34, 29.46, 29.45, 29.31, 29.59, 29.46, 29.45, 29.31], 'model': ['WWR: 0.3, Window_U: 1.4, Window_SHGC: 0.3', 'WWR: 0.2, Window_U: 1.4, Window_SHGC: 0.3', 'WWR: 0.3, Window_U: 1.6, Window_SHGC: 0.4', 'WWR: 0.3, Window_U: 1.6, Window_SHGC: 0.3', 'WWR: 0.3, Window_U: 1.4, Window_SHGC: 0.4', 'INIT', 'WWR: 0.2, Window_U: 1.6, Window_SHGC: 0.4', 'WWR: 0.2, Window_U: 1.6, Window_SHGC: 0.3', 'WWR: 0.2, Window_U: 1.4, Window_SHGC: 0.4'], 'model_plot': ['case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case8', 'case9']}
#result_unit = ""
#plot = ParametricPlot(result_dict, result_unit)
#plot.parallel_coordinate_plotly()
