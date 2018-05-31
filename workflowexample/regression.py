"""
This example shows how to use scikit-learn
with BuildSimHub parametric study object
to train a regression model

"""
import BuildSimHubAPI as bsh_api
import BuildSimHubAPI.postprocess as pp
import numpy as np
import pandas as pd

# Parametric Study

# 1. set your folder key
project_key = '7e140eec-b37f-4213-8640-88b5f96c0065'
model_key = '48003d7a-143f-45c1-b175-4ab4d1968bbd'

file_dir = "/Users/weilixu/Desktop/data/jsontest/5ZoneAirCooled_UniformLoading.epJSON"

bsh = bsh_api.BuildSimHubAPIClient()
new_pj = bsh.new_parametric_job(project_key, model_key)

# Define EEMs
wwr = bsh_api.measures.WindowWallRatio()
wwr_ratio = [0.6, 0.4]
wwr.set_datalist(wwr_ratio)

lpd = bsh_api.measures.LightLPD('ip')
lpdValue = [1.2, 0.9]
lpd.set_datalist(lpdValue)

heatEff = bsh_api.measures.HeatingEfficiency()
cop = [0.8, 0.86]
heatEff.set_datalist(cop)

# Add EEMs to parametric job
new_pj.add_model_measure(wwr)
new_pj.add_model_measure(lpd)
new_pj.add_model_measure(heatEff)

# Start!
results = new_pj.submit_parametric_study(track=True)

if results:

    # Collect results
    result_dict = results.net_site_eui()
    result_unit = results.last_parameter_unit

    # Plot
    plot = pp.ParametricPlot(result_dict, result_unit)
    df = plot.pandas_df()




class Regression(object):
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

    def add_column(self, head, col):
        """

        :param head:
        :param col:
        :type head: str
        :type col: list
        :return:
        """
        if head == 'Value':
            return False
        self._df.assign(head=col)

    def x_validate(self):
        y = self._df[['Value']]
        try:
            from sklearn.model_selection import cross_val_score
        except ImportError:
            print("Sci-kit learn package is required for model training. Please install the package at: "
                  "http://scikit-learn.org/stable/index.html")
            return
