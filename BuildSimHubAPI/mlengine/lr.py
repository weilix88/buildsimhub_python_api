"""
AUTHOR: Tracy Ruan
Modified: Weili Xu
Date: 6/30/2018

What is this script for?
This script can draw a decision tree based on the trained model.

How to use this script?
Replace the project_api_key and model_api_key in this script. Make sure that the model_api_key is the one provided
after a successful parametric run.

Specify the number of trees in the forest (n_estimate)
Specify the depth of the tree that you wish to draw

Package required:
pandas, numpy, sci-kit learn

"""
from .regressor import Regressor
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn import preprocessing


class LinearRegressor(Regressor):

    def __init__(self, df):
        Regressor.__init__(self, df)
        self._alg_name = 'Linear Regression'
        self._copied_data = self._data.copy()
        self._label_converter = dict()

    def train(self, target):
        temp_df = self._copied_data
        target_data = temp_df[target]
        del temp_df[target]
        self._header_list = list(temp_df)
        self._feature_extract(temp_df)

        # try encode categorical data
        temp_df = self._df_encoder(temp_df)
        features = np.array(temp_df)

        # retrieve from the hyper parameter spec
        test_size = 0.2

        x_train, x_test, y_train, y_test = train_test_split(features, target_data, test_size=test_size)
        self._alg = LinearRegression()
        self._alg.fit(x_train, y_train)
        prediction = self._alg.predict(x_test)

        return [metrics.mean_absolute_error(y_test, prediction), metrics.mean_squared_error(y_test, prediction)]

    def predict(self, test):
        if self._alg is None:
            return 'Error: No algorithm is trained'

        # test is json format (dict) we need to convert to
        # pandas df
        val_df = pd.DataFrame(test)
        temp_df = self._df_encoder(val_df)
        features = np.array(temp_df)
        return self._alg.predict(features)

    def _df_encoder(self, temp_df):
        categorical_df = temp_df.select_dtypes(include=[object])
        if not categorical_df.empty:
            head_list = list(categorical_df)
            for head in head_list:
                if head not in self._label_converter:
                    le = preprocessing.LabelEncoder()
                    le.fit(categorical_df[head])
                    self._label_converter[head] = le
                    temp_df[head] = le.transform(temp_df[head])
                else:
                    temp_df[head] = self._label_converter[head].transform(temp_df[head])
        return temp_df


