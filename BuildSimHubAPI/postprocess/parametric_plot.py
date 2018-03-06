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
            #data_dict['Value'] = self._value[j]

            data_list.append(data_dict)

        self._model_plot.pop(init_index)
        self._value.pop(init_index)
        self._df = pd.DataFrame(data_list, index=self._model_plot)
        self._df['Value'] = self._value

    def pandas_df(self):
        return self._df

    def line_plot(self, title):
        ind = np.arange(len(self._value))
        plt.pyplot.xticks(ind, self._model_plot)
        plt.pyplot.plot(self._value)
        plt.pyplot.ylabel(self._unit)
        plt.title(title)
        plt.pyplot.show()

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
        for i, ax in enumerate(axes):
            for idx in self._df.index:
                if hasCategory:
                    category = self._df.loc[idx, investigate]
                    ax.plot(x, self._df.loc[idx, cols], colours[category])
                else:
                    ax.plot(x, self._df.loc[idx, cols])
            ax.set_xlim([x[i], x[i + 1]])

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
        for dim, ax in enumerate(axes):
            seen.clear()
            ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))

            col_data = self._df[cols[dim]]
            for i in range(len(col_data)):
                seen.add(col_data[i])

            set_ticks_for_axis(dim, ax, len(seen))
            ax.set_xticklabels(cols[dim])

        # move the final axis' ticks to the right-hand side
        ax = plt.twinx(axes[-1])
        dim = len(axes)
        ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
        set_ticks_for_axis(dim, ax, len(seen))
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


#result_dict = {'value': [20.0, 19.81, 20.06, 19.88, 19.78, 20.28, 20.04, 20.22, 19.88, 20.52], 'model': ['Window_U: 1.6, Window_SHGC: 0.4', 'Window_U: 1.6, Window_SHGC: 0.3', 'Window_U: 1.4, Window_SHGC: 0.5', 'Window_U: 1.4, Window_SHGC: 0.4', 'Window_U: 1.4, Window_SHGC: 0.3', 'Window_U: 2.0, Window_SHGC: 0.4', 'Window_U: 2.0, Window_SHGC: 0.3', 'Window_U: 1.6, Window_SHGC: 0.5', 'INIT', 'Window_U: 2.0, Window_SHGC: 0.5'], 'model_plot': ['case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case8', 'case9', 'case10']}
#result_unit = ""
#plot = ParametricPlot(result_dict, result_unit)
#plot.parallel_coordinate("this is a test", 'Window_U')