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
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.preprocessing import LabelBinarizer


class RandomForest(Regressor):

    def __init__(self, df):
        Regressor.__init__(self, df)
        self._alg_name = 'Random Forest'
        self._copied_data = self._data.copy()
        self._hyper_param_spec['n_estimator'] = {'type': 'num', 'min': 1, 'max': 2000, 'default': 10, 'val': 10}
        self._binarizer = dict()

    def train(self, target):
        temp_df = self._copied_data
        target_data = temp_df[target]
        del temp_df[target]
        self._header_list = list(temp_df)
        self._feature_extract(temp_df)

        # encoding
        temp_df = self._df_encoder(temp_df)

        features = np.array(temp_df)

        # retrieve from the hyper parameter spec
        test_size = 0.2
        n_estimate = self._hyper_param_spec['n_estimator']['val']

        # train-test sets
        x_train, x_test, y_train, y_test = train_test_split(features, target_data, test_size=test_size)

        # train
        self._alg = RandomForestRegressor(n_estimators=n_estimate)
        self._alg.fit(x_train, y_train)
        # test
        prediction = self._alg.predict(x_test)
        return [metrics.mean_absolute_error(y_test, prediction), metrics.mean_squared_error(y_test, prediction)]

    def predict(self, test):
        """
        Override predict because we may need to re-encode the data
        :param test:
        :return:
        """
        if self._alg is None:
            return 'Error: No algorithm is trained'

        val_df = pd.DataFrame(test, index=[0])
        temp_df = self._df_encoder(val_df)
        features = np.array(temp_df)
        return self._alg.predict(features)

    def get_alg(self):
        return RandomForestRegressor(n_estimators=10)

    def _df_encoder(self, temp_df):
        # encoding
        categorical_df = temp_df.select_dtypes(include=[object])
        if not categorical_df.empty:
            # 1. INSTANTIATE
            header_list = list(categorical_df)
            for head in header_list:

                if head not in self._binarizer:
                    head_b = LabelBinarizer()
                    head_b.fit(categorical_df[head].values)
                    self._binarizer[head] = head_b
                else:
                    head_b = self._binarizer[head]

                head_b_transform = head_b.transform(categorical_df[head].values)
                if len(head_b.classes_) == 2:
                    # in this case, the encoder will assume boolean
                    temp_df[head] = head_b_transform
                else:
                    counter = 0
                    for key in head_b.classes_:
                        temp_df[key] = head_b_transform[:, counter]
                        counter += 1
                    del temp_df[head]
        return temp_df
