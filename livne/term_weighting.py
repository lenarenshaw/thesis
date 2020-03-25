# Set of candidates: U
# Candidates have a set of documents Du associated with them
# tf(t, d) term, documents => number of occurences in a document, df(t)
# V is vocabulary of the corpus
# idf(t, d) = 1/log(1 + |D|/df(t))
# udf(t, Du) = df(t, Du)/Du

from nltk.stem import PorterStemmer
from datetime import timedelta, date
import json
from collections import Counter
import math

porter = PorterStemmer()

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

def get_kl_divergence(state):

    c = Counter()

    dfs = {}
    udfs = {}

    num_docs = {'bennet': 0,
        'biden': 0,
        'bloomberg': 0,
        'buttigieg': 0,
        'gabbard': 0,
        'klobuchar': 0,
        'patrick': 0,
        'sanders': 0,
        'steyer': 0,
        'warren': 0,
        'yang': 0}

    for candidate in candidate_exits.keys():
        with open('data/candidates/tweets_' + candidate +'.json') as json_file:
            data = json.load(json_file)
            docs = 0
            lst = []
            for tweet in data:
                c = Counter()
                timestamp = tweet['timestamp'].split('T')[0].split('-')
                tweet_date = date(int(timestamp[0]), int(timestamp[1]), int(timestamp[2]))
                delta = timedelta(weeks=2)
                if tweet_date < state_elections[state] and tweet_date >= state_elections[state] - delta:
                    text = tweet['text']
                    for word in text.split(" "):
                        new_word = porter.stem(word)
                        c[new_word] += 1
                lst.append(c)
                docs += 1
            #dfs: {'buttigieg': [Counter('word': 2, 'otherword', 5...),...], ...}
            dfs[candidate] = lst
            num_docs[candidate] = docs

    # total number of documents in the entire search
    total_docs = 0
    for candidate, num in num_docs.items():
        total_docs += num

    # ('buttigieg', [Counter('word', 2...)...]...)
    for candidate, termlist in dfs.items():
        udf_dict = {}
        for ctr in termlist:
            for term, count in ctr.items():
                udf_dict[term] = (count/num_docs[candidate])
        # ('buttigieg', {'word': 3...}...)
        udfs[candidate] = udf_dict

    candidate_term_weights = {}
    marginal_probabilities = {}

    # all idfs across all docs
    idfs = {}
    # all terms and counts across all docs
    tf_ctr = Counter()
    # all udfs across all docs
    udf_ctr = {}

    for candidate, df_lst in dfs.items():
        for ctr in df_lst:
            for term, count in ctr.items():
                tf_ctr[term] += count

    for term, count in tf_ctr.items():
        udf_ctr[term] = count/total_docs
        idfs[term] = math.log(1 + total_docs/count)

    for candidate, df_lst in dfs.items():
        candidate_term_weights[candidate] = {}
        for term, count in tf_ctr.items():
            if term in udfs[candidate].keys():
                candidate_term_weights[candidate][term] = count * idfs[term] * udfs[candidate][term]

    for term, count in tf_ctr.items():
        marginal_probabilities[term] = count * udf_ctr[term]

    vocabulary = tf_ctr.keys()
    len_vocabulary = len(vocabulary)

    # normalizing values
    candidate_term_weights_normalized = {}
    for candidate, dict in candidate_term_weights.items():
        new_vals = {}
        sum = 0
        for term, val in dict.items():
            sum += val
        for term, val in dict.items():
            new_vals[term] = (val/sum)
        candidate_term_weights_normalized[candidate] = new_vals

    marginal_probabilities_normalized = {}
    sum = 0
    for term, val in marginal_probabilities.items():
        sum += val
    for term, val in marginal_probabilities.items():
        marginal_probabilities_normalized[term] = (val/sum)

    # smoothing the weights
    lam = 0.001
    smoothed_candidate_term_weights = {}
    for candidate, dict in candidate_term_weights_normalized.items():
        temp_dict = {}
        for term, term_weight in dict.items():
            temp_dict[term] = (1 - lam) * term_weight + lam * marginal_probabilities_normalized[term]
        smoothed_candidate_term_weights[candidate] = temp_dict

    # normalized smoothed weights per candidate
    final_candidate_weights = {}
    for candidate, dict in smoothed_candidate_term_weights.items():
        new_vals = {}
        sum = 0
        for term, val in dict.items():
            sum += val
        for term, val in dict.items():
            new_vals[term] = (val/sum)
        final_candidate_weights[candidate] = new_vals

    # normalized smoothed weights for the democratic party
    sum = 0
    new_vals = Counter()
    final_weights = {}
    for candidate, dict in smoothed_candidate_term_weights.items():
        for term, val in dict.items():
            new_vals[term] += val
            sum += val
    for term, val in new_vals.items():
        final_weights[term] = val/sum

    # symmetric KL divergence
    kl_values_candidates = {}
    for candidate, dict in final_candidate_weights.items():
        sum = 0
        for term, p1t in dict.items():
            p2t = final_weights[term]
            sum += ((p1t * (math.log(p1t)/math.log(p2t))) + (p2t + (math.log(p2t)/math.log(p1t))))
        kl_values_candidates[candidate] = {'kl_divergence': sum}

    return kl_values_candidates
