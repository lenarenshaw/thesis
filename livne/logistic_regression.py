import pandas as pd
from pymongo import MongoClient
import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.utils.fixes import signature
from sklearn.metrics import confusion_matrix
import seaborn as sns
import calendar

from sklearn.neural_network import MLPClassifier

import math
import re

client = MongoClient('mongodb+srv://lenarenshaw:qwerty12@renshawthesis2-spgqz.mongodb.net/test?retryWrites=true&w=majority')

politics_db = client['politics_db']
anes_voter_survey = politics_db['anes_voter_survey']

def mongo_to_df():
    """
    Converts db_cases to a pandas df
    :return: pandas df
    """
    print("creating dataframe...")
    full_list = anes_voter_survey.find()[0:100]
    tmp_lst = []
    i = 0
    for data in full_list:
        tmp_lst.append(data)
        i += 1

    df = pd.DataFrame(tmp_lst)
    print("finished creating dataframe...")
    # print(df.iloc[10000]) # prints the 0th row from the pandas df

    return df

    """
    # helpful other commands to look at data
    print(db_cases.find_one()) # prints one case from the mongo db
    print(df.iloc[0]) # prints the 0th row from the pandas df
    """

def convert_data(df):
    data = []
    columns = df.columns
    for index, row in df.iterrows():
        tmp = {}
        for col in columns:
            if col != 'lat' and col != 'lon':
                tmp[col] = row[col]
        data.append(tmp)
    return data

def clean_data(data):
    ml_data = []
    labels = []
    feature_list = []
    feature_dict = dict()
    no_use_keys = set()
    i = 0
    for row in data:
        tmp = []
        for key, value in row.items():
            if key not in no_use_keys:
                feature_list.append(key)
                feature_dict[key] = (i, i+1)
                if isinstance(value, str):
                    try:
                        tmp.append(float(value[0][0]))
                    except ValueError:
                        no_use_keys.add(key)
                else:
                    try:
                        if math.isnan(float(value)):
                            no_use_keys.add(key)
                        else:
                            tmp.append(float(value))
                    except ValueError:
                        no_use_keys.add(key)
                    except TypeError:
                        no_use_keys.add(key)
        ml_data.append(tmp)
    print("finished cleaning data")
    svd = TruncatedSVD(n_iter=7)

    ml_data = []
    labels = []
    feature_list = []
    for row in data:
        tmp = []
        for key, value in row.items():
            if key not in no_use_keys:
                if key not in feature_list:
                    feature_list.append(key)
                if isinstance(value, str):
                    try:
                        tmp.append(float(value[0][0]))
                    except ValueError:
                        no_use_keys.add(key)
                else:
                    try:
                        if math.isnan(float(value)):
                            no_use_keys.add(key)
                        else:
                            tmp.append(float(value))
                    except ValueError:
                        no_use_keys.add(key)
                    except TypeError:
                        no_use_keys.add(key)
        ml_data.append(tmp)
        print(len(tmp))

    i = 0
    feature_dict = dict()
    for key in feature_list:
        feature_dict[key] = (i, i+1)
        i = i+1

    # reduced_data = svd.fit_transform(np.array(ml_data))
    print("created svd")
    return np.array(ml_data), np.array(np.random.choice([0, 1], size=100)), feature_list, feature_dict

"""
TODOs:
0. Convert mongo db_cases into a pandas dataframe
1. Convert all features to columns
2. LogisticRegression.train(data)
    a. class_weight = balanced
3. Get new data, put in db as db_test_cases, db_test_arrests
    instead, use train_test_split method from sklearn
4. LogisticRegression.train(test_data)
5. Analyze results:
    a. Make precision-recall graph
"""

def balance(X_train, y_train):
    """
    Attempt to throw out a ton of data so its an even split.
    Results in high recall but horrible precision (<0.3)
    :param X_train:
    :param y_train:
    :return:
    """
    num_arrests = sum(y_train)
    print(y_train.shape)
    num_non_arrests = len(y_train) - 2 * num_arrests
    print("num_arrests:", num_arrests)

    train = np.hstack((X_train, np.expand_dims(y_train, axis=1)))
    masked_idxs = []
    for i in range(len(y_train)):
        if y_train[i] == 0:
             masked_idxs.append(i)
        if len(masked_idxs) >= num_non_arrests:
            break

    print("masked_idxs:", len(masked_idxs))
    masked_idxs = np.array(masked_idxs)

    m = np.zeros_like(train)
    m[masked_idxs, :] = 1

    masked_train = np.ma.compress_rows(np.ma.masked_array(train, m))

    new_X_train = masked_train[:, :-1]
    new_y_train = masked_train[:, -1]
    print("new x train shape:", new_X_train.shape)

    return new_X_train, new_y_train


def plot_coefs_std(std_coef, feature_list, feature_dict):
    # plot all features
    # sns.barplot(feature_list, std_coef)
    # plt.xticks(rotation=90)
    # plt.show()
    sns.barplot([feature_list[i] for i in range(0, len(feature_list)) if np.abs(std_coef[i]) > 0.1],
                [std_coef[i] for i in range(0, len(feature_list)) if np.abs(std_coef[i]) > 0.1])
    plt.xticks(rotation=90)
    plt.title("Weights across most significant features", fontsize=22)
    plt.xlabel("Feature")
    plt.ylabel("coef * std")
    plt.show()


def train_and_test(X, y, feature_list, feature_dict):
    """
    Method to train and test on our data!
    :param X: pandas df of the features
    :param y: some form of a list/nparray/df of the labels, ordered in the same way as X
    :return: the accuracy/score of the model!
    """
    # print(X[0:10])
    print(X)
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        train_size=0.8,
        # random_state=0,
        # shuffle=True
    )

    # new_X_train, new_y_train = balance(X_train, y_train)
    # X_test, y_test = balance(X_test, y_test)

    class_weights = {0: 0.9, 1: 0.1}
    model = RandomForestClassifier(random_state=0).fit(X_train, y_train)
    # print("coefs:", model.coef_)
    std_coef = (np.std(X_train, 0) * model.coef_)[0]
    # print(len(std_coef))
    # print(len(feature_list))
    # print("coefs * std max:", np.argmax(np.std(X_train, 0) * model.coef_))
    # print("coefs * std min:", np.argmin(np.std(X_train, 0) * model.coef_))

    plot_coefs_std(std_coef, feature_list, feature_dict)
    # sns.barplot(feature_list, std_coef)
    # plt.xticks(rotation=90)
    # plt.show()
    score = model.score(X_test, y_test)
    print("Score:", score)
    type12errs = type_1_2_errors(model, X_test, y_test)
    precision = type12errs["precision"]
    recall = type12errs["recall"]
    print(type12errs)
    precision_recall(model, X_test, y_test)

    return score, precision, recall

def feature_importance(model, features_dict):
    pass

def precision_recall(model, X_test, y_test):
    y_score = model.decision_path(X_test)
    average_precision = average_precision_score(y_test, y_score)
    print('Average precision-recall score: {0:0.2f}'.format(
        average_precision))
    precision, recall, _ = precision_recall_curve(y_test, y_score)

    # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
    step_kwargs = ({'step': 'post'}
                   if 'step' in signature(plt.fill_between).parameters
                   else {})
    plt.step(recall, precision, color='b', alpha=0.2,
             where='post')
    plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
              average_precision))
    plt.show()

def type_1_2_errors(model, X_test, y_test):
    preds = model.predict(X_test)
    FP = confusion_matrix(y_test, preds)[0][1]
    FN = confusion_matrix(y_test, preds)[1][0]
    TP = confusion_matrix(y_test, preds)[1][1]
    TN = confusion_matrix(y_test, preds)[0][0]

    precision = TP/(TP + FP)
    recall = TP/(TP + FN)

    return {"False positive": FP,
            "False negative": FN,
            "True positive": TP,
            "True Negative": TN,
            "precision": precision,
            "recall": recall}

def main():
    # score_list = []
    # precision_list = []
    # recall_list = []
    data = [['tom', 10], ['nick', 15], ['juli', 14]]
    df = pd.DataFrame(data, columns = ['Name', 'Age'])

    # df = mongo_to_df()
    data = convert_data(df)

    ml_data, labels, feature_list, feature_dict = clean_data(data)

    score, precision, recall = train_and_test(ml_data, labels, feature_list, feature_dict)
    # score_list.append(score)
    # precision_list.append(precision)
    # recall_list.append(recall)
    # avg_score = np.mean(score_list)
    # avg_precision = np.mean(precision_list)
    # avg_recall = np.mean(recall_list)
    # print("Avg score:", avg_score)
    # print("Avg precision:", avg_precision)
    # print("Avg recall:", avg_recall)

if __name__ == "__main__":
    main()
