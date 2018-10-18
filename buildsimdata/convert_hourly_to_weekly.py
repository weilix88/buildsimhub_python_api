# https://github.com/yzhao062/Pyod
# pyod documentation
import pandas as pd
from datetime import datetime as dt
import logging
import calendar
import matplotlib.pyplot as plt
import numpy as np
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.pca import PCA


# from pyod.models.mcd import MCD
# from pyod.models.cblof import CBLOF
# from pyod.models.hbos import HBOS


def generate_df_frame(processedarr, num):
    plot_df = pd.DataFrame(
        {'x': range(0, 24), 'Monday': np.asarray(processedarr[num][0]), 'Tuesday': np.asarray(processedarr[num][1]),
         'Wednesday': np.asarray(processedarr[num][2]), 'Thursday': np.asarray(processedarr[num][3]),
         'Friday': np.asarray(processedarr[num][4]), 'Saturday': np.asarray(processedarr[num][5]),
         'Sunday': np.asarray(processedarr[num][6])})
    return plot_df


def generate_graph(row_fields, data_after):
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')

    num = 0
    for index in range(len(row_fields) - 1):
        plt_df = generate_df_frame(data_after, num)
        num += 1
        plt.subplot(3, 3, num)
        i = 0
        for v in plt_df.drop('x', axis=1):
            plt.plot(plt_df['x'], plt_df[v], marker='', color=palette(i), linewidth=2.4, alpha=0.9,
                     label=row_fields[index + 1])
            i = i + 1

    plt.suptitle("Plot of average lighting power consuption at different hour across different days", fontsize=13,
                 fontweight=0, color='black', style='italic', y=1.02)
    plt.show()


def main(model_selector):
    model = {1: KNN(), 2: LOF(), 3: PCA()}
    df = pd.read_csv('pow_lighting.csv')  # original dataframe
    df = df.dropna()  # adter remove na row
    row_fields = df.keys()  # the data fields
    data_store = []  # store the df data fields -> weekday -> hour
    no_outlier = []  # store the inliner data
    data_after = []  # calc the average of each hours' data and use it to generate graph
    for i in range(1, len(row_fields)):
        data_store.append(list())
        no_outlier.append(list())
        data_after.append(list())
        for j in range(7):
            data_store[i - 1].append(list())
            no_outlier[i - 1].append(list())
            data_after[i - 1].append(list())
            data_after[i - 1][j] = []
            for z in range(24):
                data_store[i - 1][j].append(list())
                no_outlier[i - 1][j].append(list())

    for index, row in df.iterrows():
        date_str = row[row_fields[0]]
        templist = date_str.split('/')
        date_str = templist[0] + '/' + templist[1] + '/20' + templist[2]
        date_obj = dt.strptime(date_str, '%m/%d/%Y %H:%M')
        weekday = date_obj.weekday()
        hour_in_date = date_obj.hour
        for m in range(1, len(row_fields)):
            data_store[m - 1][weekday][hour_in_date].append(row[row_fields[m]])

    for i in range(len(data_store)):
        for j in range(len(data_store[i])):
            for z in range(len(data_store[i][j])):
                clf = model[model_selector]
                X_train = np.asarray(data_store[i][j][z]).reshape(-1, 1)
                clf.fit(X_train)
                y_train_pred = clf.labels_
                for index in range(len(data_store[i][j][z])):
                    if y_train_pred[index] == 0:
                        no_outlier[i][j][z].append(data_store[i][j][z][index])

    for i in range(len(data_store)):
        for j in range(len(data_store[i])):
            for z in range(len(data_store[i][j])):
                data_after[i][j].append(float(sum(no_outlier[i][j][z]) / len(no_outlier[i][j][z])))

    generate_graph(row_fields, data_after)


main(1)
