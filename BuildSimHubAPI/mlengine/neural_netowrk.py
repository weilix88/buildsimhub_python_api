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
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelBinarizer
from sklearn.neural_network import MLPRegressor
from sklearn import metrics


class NeuralNetwork(Regressor):

    def __init__(self, df):
        Regressor.__init__(self, df)
        self._alg_name = 'Neural Network'
        self._copied_data = self._data.copy()
        self._scaler = StandardScaler()
        self._hyper_param_spec['std_scale'] = {'type': 'bool', 'default': 'no', 'val': 'no'}
        self._hyper_param_spec['regularization'] = {'type': 'num', 'min': 1**-5, 'max': 1000,
                                                    'default': 1**-5, 'val': 1**-5}
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
        # self._scaler.fit(features)
        # ML perceptron is sensitive to feature scaling - scale each attribute on the input
        # vector to [0,1]
        # retrieve from the hyper parameter spec
        test_size = 0.2
        x_train, x_test, y_train, y_test = train_test_split(features, target_data, test_size=test_size)
        # x_train = self._scaler.transform(x_train)
        self._alg = MLPRegressor(solver='lbfgs', alpha=1e-5,
                                 hidden_layer_sizes=(5, 2), random_state=1)
        self._alg.fit(x_train, y_train)

        # x_test = self._scaler.transform(x_test)
        prediction = self._alg.predict(x_test)

        return [metrics.mean_absolute_error(y_test, prediction), metrics.mean_squared_error(y_test, prediction)]

    def predict(self, test):
        """
        Override predict because we may need to re-regularize the data
        :param test:
        :return:
        """
        if self._alg is None:
            return 'Error: No algorithm is trained'

        val_df = pd.DataFrame(test)
        temp_df = self._df_encoder(val_df)
        features = np.array(temp_df)
        # features = self._scaler.transform(features)
        return self._alg.predict(features)

    def get_alg(self):
        return MLPRegressor(solver='lbfgs', alpha=1e-5,
                                 hidden_layer_sizes=(5, 2), random_state=1)

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

