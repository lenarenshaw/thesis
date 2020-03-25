results2016 = {'iowa': 'clinton',
    'newhampshire': 'sanders',
    'nevada': 'clinton',
    'southcarolina': 'clinton',
    'alabama': 'clinton',
    'americansamoa': 'clinton',
    'arkansas': 'clinton',
    'colorado': 'sanders',
    'georgia': 'clinton',
    'masssachusetts': 'clinton',
    'minnesota': 'sanders',
    'oklahoma': 'sanders',
    'tennessee': 'clinton',
    'texas': 'clinton',
    'vermont': 'sanders',
    'virginia': 'clinton',
    'kansas': 'sanders',
    'louisiana': 'clinton',
    'nebraska': 'sanders',
    'maine': 'sanders',
    'democratsabroad': 'sanders',
    'michigan': 'sanders',
    'mississippi': 'clinton'}

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

def get_tweet_parties(state):
    res = {}
    for candidate in candidates.keys():
        incumbent = 0
        if candidate == 'biden':
            incumbent = 1
        same_party = 0
        if results2016[state] == 'clinton' and candidates[candidate] == 'moderate':
            same_party = 1
        if results2016[state] == 'sanders' and candidates[candidate] == 'liberal':
            same_party = 1
        res[candidate] = {'incumbent': incumbent, 'same_party': same_party}
    return res
