import networkx as nx
from datetime import timedelta, date
import json
from collections import Counter
from matplotlib import pyplot as plt
from numpy.random import randint

# TODO:
# 1. Scrape all of the tweets from each candidate from 2 weeks prior to the first election until now.
# 2. Create a map of all of the states and the dates their eleciton occured on.
# 3. Compare the timestamps so you get tweets from the correct time up until the election (using timedelta)
# 4. Input will be the name of a state. Output will be the graph representing the 'state of the world' during that time
# 5. Add two separate methods for getting pagerank and HITS authority.

state = 'alabama'

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

candidates = {'bennet':'michaelbennet',
    'biden': 'joebiden',
    'bloomberg': 'mikebloomberg',
    'buttigieg': 'petebuttigieg',
    'gabbard': 'tulsigabbard',
    'klobuchar': 'amyklobuchar',
    'patrick': 'devalpatrick',
    'sanders':'berniesanders',
    'steyer': 'tomsteyer',
    'warren': 'ewarren',
    'yang': 'andrewyang'}

aliases = {'bennet':['bennet', 'michaelbennet'],
    'biden': ['joe', 'biden','joebiden'],
    'bloomberg': ['bloomberg', 'mike', 'mikebloomberg'],
    'buttigieg': ['buttigieg', 'pete', 'petebuttigieg'],
    'gabbard': ['tulsi', 'gabbard', 'tulsigabbard'],
    'klobuchar': ['amy', 'klobuchar', 'amyklobuchar'],
    'patrick': ['deval', 'patrick', 'devalpatrick'],
    'sanders':['bernie', 'sanders', 'berniesanders'],
    'steyer': ['tom', 'steyer', 'tomsteyer'],
    'warren': ['elizabeth', 'liz', 'warren' 'ewarren'],
    'yang': ['andrew', 'yang', 'andrewyang']}

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

c = Counter()

for candidate in candidates.keys():
    with open('data/candidates/tweets_' + candidate +'.json') as json_file:
        data = json.load(json_file)
        for tweet in data:
            text = tweet['text'].lower()
            timestamp = tweet['timestamp'].split('T')[0].split('-')
            tweet_date = date(int(timestamp[0]), int(timestamp[1]), int(timestamp[2]))
            delta = timedelta(weeks=2)
            if tweet_date < state_elections[state] and tweet_date >= state_elections[state] - delta:
                for name, alt in aliases.items():
                    if candidate_exits[name] >= state_elections[state]:
                        if name != candidate:
                            for alias in alt:
                                if alias in text:
                                    c[(candidate, name)] += 1


    with open('data/candidates/' + candidate +'_following.csv') as file:
        for line in file:
            for name, alt in aliases.items():
                handle = alt[-1]
                if line.lower() == handle:
                    c[(candidate, name)] += 1

G = nx.DiGraph()
num_nodes = 0
for candidate in candidates.keys():
    if candidate_exits[candidate] >= state_elections[state]:
        G.add_node(candidate)

for connection, weight in c.items():
    if candidate_exits[connection[0]] >= state_elections[state] and candidate_exits[connection[1]] >= state_elections[state]:
        G.add_edge(connection[0], connection[1], weight=1/weight )

drawing = nx.draw(G, with_labels = True, font_size = 8)
plt.draw()
plt.show()
