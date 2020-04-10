import sys
from datetime import date, timedelta
import csv

# if len(sys.argv) != 2:
#     print("Usage: python3 calculate_sentiment.py <state-name>")
# state = sys.argv[1]

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

states = ['iowa', 'newhampshire', 'nevada', 'southcarolina', 'alabama', 'arkansas', 'california', 'colorado', 'maine', 'massachusetts', 'minnesota', 'northcarolina', 'oklahoma', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'idaho', 'michigan', 'mississippi', 'missouri', 'washington', 'arizona', 'florida', 'illinois']

for state in states:
    dates = {}
    keywords = ['bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang']

    for topic in keywords:
        if candidate_exits[topic] >= state_elections[state]:
            file = open('data/' + state + '/raw_tweets/' + topic + '.txt')
            tweets = []
            cstart = 0
            cend = 0
            for line in file:
                cend = cend + len(line)
                tweets.append([line, cstart, cend])
                cstart = cend

            file = open('data/' + state + '/raw_tweets/' + topic + '-timestamp.txt')
            tweets_times = []
            l = 0
            for line in file:
                tweets_times.append([tweets[l] + [line]])
                l = l + 1

            file = open('data/' + state + '/oconnor/' + topic + '.txt_auto_anns/subjcluesSentenceClassifiersOpinionFinderJune06', 'r')

            for line in file:
                arr = line.split(' ')
                type = arr[-1].split('\"')[1]
                range_start = int(arr[0].split("\t")[1].split(",")[0])
                range_end = int(arr[0].split("\t")[1].split(",")[1])
                for lst in tweets_times:
                    if range_start >= lst[0][1] and range_end <= lst[0][2]:
                        pos = 0
                        neg = 0
                        if type == 'strongpos':
                            pos = 1
                        elif type == 'weakpos':
                            pos = 1
                        elif type == 'strongneg':
                            neg = 1
                        elif type == 'weakneg':
                            neg = 1

                        day = lst[0][3]
                        day = day.replace("\n", "")

                        if day not in dates.keys():
                            dates[day] = {}
                        dct = dates[day]
                        if topic not in dct.keys():
                            dct[topic] = (pos, neg)
                        else:
                            p, n = dct[topic]
                            dct[topic] = (p + pos, n + neg)
                        dates[day] = dct

    with open('data/' + state + '/oconnor/dated-sentiment-results.csv', 'w') as csv_file:
        three_weeks_prior = state_elections[state] - timedelta(days=21)
        writer = csv.writer(csv_file, delimiter=',')
        header = ['date']
        for candidate in candidate_exits.keys():
            header.append(candidate)
        writer.writerow(header)
        for i in range(21):
            day = str(three_weeks_prior + timedelta(days=i))
            if day in dates.keys():
                results = dates[day]
                lst = [day]
                for candidate in candidate_exits.keys():
                    if candidate in results.keys():
                        pos, neg = results[candidate]
                        if neg == 0:
                            lst.append(pos)
                        else:
                            lst.append(pos/neg)
                    else:
                        lst.append(0)
                writer.writerow(lst)
