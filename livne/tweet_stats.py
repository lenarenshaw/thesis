from datetime import timedelta, date
import json
from collections import Counter

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

def get_tweet_stats(state):
    res = {}
    for candidate in candidate_exits.keys():
        with open('data/candidates/tweets_' + candidate +'.json') as json_file:
            data = json.load(json_file)
            num_tweets = 0
            hashtags = Counter()
            replies = 0
            retweets = 0
            for tweet in data:
                timestamp = tweet['timestamp'].split('T')[0].split('-')
                tweet_date = date(int(timestamp[0]), int(timestamp[1]), int(timestamp[2]))
                delta = timedelta(weeks=2)
                if tweet_date < state_elections[state] and tweet_date >= state_elections[state] - delta:
                    num_tweets += 1
                    replies += tweet['replies']
                    retweets += tweet['retweets']
                    for hashtag in tweet['hashtags']:
                        hashtags[hashtag] += 1
                replies_average = 0
                retweets_average = 0
                if num_tweets != 0:
                    replies_average = replies/num_tweets
                    retweets_average = retweets/num_tweets
            common_hashtags = []
            for hashtag in hashtags.most_common(10):
                common_hashtags.append(hashtag[0])

        # currently removed hashtags: 'hashtags': common_hashtags,

        res[candidate] = {'tweets': num_tweets, 'replies_total': replies, 'replies_average': replies_average, 'retweets_total': retweets, 'retweets_average': retweets_average}
    return res
