import networkx as nx
from datetime import timedelta, date
import json
from collections import Counter
from matplotlib import pyplot as plt
from numpy.random import randint

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

def candidates_and_aliases(state):
    candidates_in = {}
    aliases_in = {}

    for candidate in candidates.keys():
        if candidate_exits[candidate] >= state_elections[state]:
            candidates_in[candidate] = candidates[candidate]
            aliases_in[candidate] = aliases[candidate]
    return candidates_in, aliases_in

def create_graph(state):
    c = Counter()

    candidates_in, aliases_in = candidates_and_aliases(state)

    for candidate in candidates_in.keys():
        with open('data/candidates/tweets_' + candidate +'.json') as json_file:
            data = json.load(json_file)
            for tweet in data:
                text = tweet['text'].lower()
                timestamp = tweet['timestamp'].split('T')[0].split('-')
                tweet_date = date(int(timestamp[0]), int(timestamp[1]), int(timestamp[2]))
                delta = timedelta(weeks=2)
                if tweet_date < state_elections[state] and tweet_date >= state_elections[state] - delta:
                    for name, alt in aliases_in.items():
                        if name != candidate:
                            for alias in alt:
                                if alias in text:
                                    c[(candidate, name)] += 1


        with open('data/candidates/' + candidate +'_following.csv') as file:
            for line in file:
                for name, alt in aliases_in.items():
                    handle = alt[-1]
                    if line.lower() == handle:
                        c[(candidate, name)] += 1

    G = nx.DiGraph()
    num_nodes = 0
    for candidate in candidates_in.keys():
        G.add_node(candidate)

    for connection, weight in c.items():
        G.add_edge(connection[0], connection[1], weight=1/weight )

    # drawing = nx.draw(G, with_labels = True, font_size = 8)
    # plt.draw()
    # plt.show()
    return G

def closeness_helper(G, state, is_incoming):
    which_edge = 0
    if is_incoming:
        which_edge = 1
    edges = Counter()
    num_edges = Counter()
    res = {}
    for edge in G.edges.data('weight'):
        edges[edge[which_edge]] += edge[2]
        num_edges[edge[which_edge]] += 1

    candidates_in, aliases_in = candidates_and_aliases(state)

    for candidate in candidates_in.keys():
        if candidate in edges.keys():
            res[candidate] = num_edges[candidate] / edges[candidate]
        else:
            res[candidate] = 0

    return res

def closeness_in(G, state):
    return closeness_helper(G, state, True)

def closeness_out(G, state):
    return closeness_helper(G, state, False)

def closeness_all(G, state):
    edges = Counter()
    num_edges = Counter()
    res = {}
    for edge in G.edges.data('weight'):
        edges[edge[0]] += edge[2]
        edges[edge[1]] += edge[2]
        num_edges[edge[0]] += 1
        num_edges[edge[1]] += 1
    candidates_in, aliases_in = candidates_and_aliases(state)
    for candidate in candidates_in.keys():
        if candidate in edges.keys():
            res[candidate] = num_edges[candidate] / edges[candidate]
        else:
            res[candidate] = float('inf')
    return res

def in_degree(G, state):
    res = {}
    for node in list(G.nodes):
        res[node] = G.in_degree[node]
    return res

def out_degree(G, state):
    res = {}
    for node in list(G.nodes):
        res[node] = G.out_degree[node]
    return res

def get_graph_calculations(state):
    G = create_graph(state)
    close_in = closeness_in(G, state)
    close_out = closeness_out(G, state)
    close_all = closeness_all(G, state)
    pr = nx.pagerank(G)
    hit = nx.hits(G)[0]
    in_deg = in_degree(G, state)
    out_deg = out_degree(G, state)

    res = {}
    candidates_in, aliases_in = candidates_and_aliases(state)
    for candidate in candidates_in.keys():
        res[candidate] = {'closeness_in': close_in[candidate], 'closeness_out': close_out[candidate], 'closeness_all': close_all[candidate], 'pagerank': pr[candidate],'hits': hit[candidate],'in_degree': in_deg[candidate],'out_degree': out_deg[candidate]}
    return res
