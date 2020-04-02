# Credits to https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8 for the great logistic regression guide!

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

from create_candidate_graph import get_graph_calculations, candidates_and_aliases
from term_weighting import get_kl_divergence
from tweet_parties import get_tweet_parties
from tweet_stats import get_tweet_stats

MAX_VAL = 1000000
candidates = {'bennet':'michaelbennet',
    'biden': 'moderate',
    'bloomberg': 'moderate',
    'buttigieg': 'moderate',
    'gabbard': 'liberal',
    'klobuchar': 'moderate',
    'patrick': 'moderate',
    'sanders':'liberal',
    'steyer': 'moderate',
    'warren': 'liberal',
    'yang': 'moderate'}

results2020 = {'iowa': 'buttigieg',
    'newhampshire': 'sanders',
    'nevada': 'sanders',
    'southcarolina': 'biden',
    'alabama': 'biden',
    'arkansas': 'biden',
    'colorado': 'sanders',
    'massachusetts': 'biden',
    'minnesota': 'biden',
    'oklahoma': 'biden',
    'tennessee': 'biden',
    'texas': 'biden',
    'vermont': 'sanders',
    'virginia': 'biden',
    'maine': 'biden',
    'michigan': 'biden',
    'mississippi': 'biden'}

candidate_features = []
for state in results2020.keys():
    print(state)

    graph_fields = get_graph_calculations(state)
    term_fields = get_kl_divergence(state)
    party_fields = get_tweet_parties(state)
    stat_fields = get_tweet_stats(state)

    candidates_in, aliases_in = candidates_and_aliases(state)

    for candidate in candidates_in.keys():
        won = 0
        if candidate == results2020[state]: won = 1
        candidate_features.append({**graph_fields[candidate], **term_fields[candidate], **party_fields[candidate], **stat_fields[candidate], "won": won})

df_dict = {}
for features in candidate_features:
    for feature, value in features.items():
        if feature in df_dict.keys():
            temp = df_dict[feature]
            if np.isinf(value):
                value = MAX_VAL
            temp.append(value)
            df_dict[feature] = temp
        else:
            df_dict[feature] = [value]

data_final = pd.DataFrame.from_dict(df_dict)
data_final = data_final.fillna(0)

X = data_final.loc[:, data_final.columns != 'won']
y = data_final.loc[:, data_final.columns == 'won']

from imblearn.over_sampling import SMOTE
os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

columns = X_train.columns
os_data_X,os_data_y=os.fit_sample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['won'])

print("length of oversampled data is ",len(os_data_X))
print("Number of no subscription in oversampled data",len(os_data_y[os_data_y['won']==0]))
print("Number of subscription",len(os_data_y[os_data_y['won']==1]))
print("Proportion of no subscription data in oversampled data is ",len(os_data_y[os_data_y['won']==0])/len(os_data_X))
print("Proportion of subscription data in oversampled data is ",len(os_data_y[os_data_y['won']==1])/len(os_data_X))

data_final_vars=data_final.columns.values.tolist()
from sklearn.feature_selection import RFE
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)

X=os_data_X[columns]
y=os_data_y['won']

import statsmodels.api as sm
x_train1 = sm.add_constant(X_train)
lm_1 = sm.OLS(y_train, X_train).fit()
print(lm_1.summary())

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
logreg = LogisticRegression()
result = logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)
