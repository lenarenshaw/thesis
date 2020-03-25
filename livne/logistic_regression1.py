import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)




# import pandas as pd
# import datetime
# from sklearn.linear_model import LogisticRegression
# from sklearn import metrics
#
# def convert_data(df):
#     data = []
#     columns = df.columns
#     for index, row in df.iterrows():
#         tmp = {}
#         for col in columns:
#             tmp[col] = row[col]
#         data.append(tmp)
#     return data
#
# def clean_data(data):
#     ml_data = []
#     labels = []
#     feature_list = []
#     feature_dict = dict()
#     no_use_keys = set()
#     i = 0
#     for row in data:
#         tmp = []
#         for key, value in row.items():
#             if key not in no_use_keys:
#                 feature_list.append(key)
#                 feature_dict[key] = (i, i+1)
#                 tmp.append(float(value))
#         ml_data.append(tmp)
#
#     i = 0
#     feature_dict = dict()
#     for key in feature_list:
#         feature_dict[key] = (i, i+1)
#         i = i+1
#
#     return np.array(ml_data), np.array(np.random.choice([0, 1], size=3)), feature_list, feature_dict
#
# def train_and_test(X, y):
#     X_train, X_test, y_train, y_test = train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         train_size=0.8,
#         # random_state=0,
#         shuffle=True
#     )
#
#     logreg = LogisticRegression()
#     logreg.fit(X_train, y_train)
#     y_pred = logreg.predict(X_test)
#     print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
#
# def precision_recall(model, X_test, y_test):
#     y_score = model.decision_path(X_test)
#     average_precision = average_precision_score(y_test, y_score)
#     print('Average precision-recall score: {0:0.2f}'.format(
#         average_precision))
#     precision, recall, _ = precision_recall_curve(y_test, y_score)
#
#     # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
#     step_kwargs = ({'step': 'post'}
#                    if 'step' in signature(plt.fill_between).parameters
#                    else {})
#     plt.step(recall, precision, color='b', alpha=0.2,
#              where='post')
#     plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)
#
#     plt.xlabel('Recall')
#     plt.ylabel('Precision')
#     plt.ylim([0.0, 1.05])
#     plt.xlim([0.0, 1.0])
#     plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
#               average_precision))
#     plt.show()
#
# def type_1_2_errors(model, X_test, y_test):
#     preds = model.predict(X_test)
#     FP = confusion_matrix(y_test, preds)[0][1]
#     FN = confusion_matrix(y_test, preds)[1][0]
#     TP = confusion_matrix(y_test, preds)[1][1]
#     TN = confusion_matrix(y_test, preds)[0][0]
#
#     precision = TP/(TP + FP)
#     recall = TP/(TP + FN)
#
#     return {"False positive": FP,
#             "False negative": FN,
#             "True positive": TP,
#             "True Negative": TN,
#             "precision": precision,
#             "recall": recall}
#
# def main():
#     # score_list = []
#     # precision_list = []
#     # recall_list = []
#     data = [['tom', 10, 10000], ['nick', 15, 20000], ['juli', 14, 30000]]
#     df = pd.DataFrame(data, columns = ['Name', 'Age', 'Income'])
#
#     # df = mongo_to_df()
#     data = convert_data(df)
#
#     ml_data, labels, feature_list, feature_dict = clean_data(data)
#
#     score, precision, recall = train_and_test(ml_data, labels, feature_list, feature_dict)
#     # score_list.append(score)
#     # precision_list.append(precision)
#     # recall_list.append(recall)
#     # avg_score = np.mean(score_list)
#     # avg_precision = np.mean(precision_list)
#     # avg_recall = np.mean(recall_list)
#     # print("Avg score:", avg_score)
#     # print("Avg precision:", avg_precision)
#     # print("Avg recall:", avg_recall)
#
# if __name__ == "__main__":
#     main()
