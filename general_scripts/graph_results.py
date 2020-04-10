import csv
import math
from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

test = 'oconnor'
state = 'washington'

candidate_exits = {'bennet':date(2020, 2, 11),
    'biden': date(2021, 1, 1), #not out
    'bloomberg': date(2020, 3, 4),
    'buttigieg': date(2020, 3, 1),
    'gabbard': date(2020, 3, 19),
    'klobuchar': date(2020, 3, 2),
    'patrick': date(2020, 2, 12),
    'sanders':date(2021, 1, 1), #not out
    'steyer': date(2020, 2, 9),
    'warren': date(2020, 3, 5),
    'yang': date(2020, 2, 11)}

state_elections = {
    #year, month, day
    'iowa': date(2020, 2, 3),
    'newhampshire': date(2020, 2, 11),
    'nevada': date(2020, 2, 22),
    'southcarolina': date(2020, 2, 29),
    'alabama': date(2020, 3, 3),
    'americansamoa': date(2020, 3, 3),
    'arkansas': date(2020, 3, 3),
    'california': date(2020, 3, 3),
    'colorado': date(2020, 3, 3),
    'maine': date(2020, 3, 3),
    'massachusetts': date(2020, 3, 3),
    'minnesota': date(2020, 3, 3),
    'northcarolina': date(2020, 3, 3),
    'oklahoma': date(2020, 3, 3),
    'tennessee': date(2020, 3, 3),
    'texas': date(2020, 3, 3),
    'utah': date(2020, 3, 3),
    'vermont': date(2020, 3, 3),
    'virginia': date(2020, 3, 3),
    'idaho': date(2020, 3, 10),
    'michigan': date(2020, 3, 10),
    'mississippi': date(2020, 3, 10),
    'missouri': date(2020, 3, 10),
    'northdakota': date(2020, 3, 10),
    'washington': date(2020, 3, 10),
    'guam': date(2020, 3, 14),
    'northernmariana': date(2020, 3, 14),
    'arizona': date(2020, 3, 17),
    'florida': date(2020, 3, 17),
    'illinois': date(2020, 3, 17)
}

election_results = {}
test_results = {}
total_delegates = 0
with open('data/' + state + '/election_results/' + state + '.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    line = next(reader, None)
    while line:
        votes = float(line['Total S.D.E.s*'].replace("\"", "").replace("\'", "").replace(",",""))
        candidate_name = line['Candidate'].split(" ")[0].lower()
        election_results[candidate_name] = votes
        total_delegates += votes
        line = next(reader, None)

total_sentiment = 0
with open('data/' + state + '/'+ test + '/results/results.txt', 'r') as file:
    for line in file:
        arr = line.split(" ")
        if arr[0] in election_results.keys():
            res = float(arr[-1])
            test_results[arr[0]] = float(arr[-1])
            total_sentiment += float(arr[-1])

keys = []
election = []
test = []

for key in election_results.keys():
    if key in test_results.keys() and candidate_exits[key] >= state_elections[state]:
        keys.append(key)
        election.append(election_results[key])
        test.append(test_results[key])

tmp = np.asarray(test)
tmp = tmp / sum(tmp)
test = list(tmp)

tmp = np.asarray(election)
tmp = tmp / sum(tmp)
election = list(tmp)

results = pd.DataFrame({"Election Results": election, "Test Results": test}, index=keys)
lines = results.plot.bar()
plt.show()
