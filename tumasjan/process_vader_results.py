from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import sys

if len(sys.argv) != 2:
    print("Usage: python3 process_vader_results.py <state-name>")
state = sys.argv[1]

# keywords = ['bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang', 'democrat', 'dem', 'caucus', 'primary']
keywords = ['biden', 'gabbard', 'sanders']
candidates = ['biden', 'gabbard', 'sanders']

all_scores = {}
all_scores_length = {}
lengths = {}
total_tweets = 0
for topic in keywords:
    with open('data/' + state + '/tumasjan/' + topic + '_polarity.json', 'r') as file:
        pos = 0
        neg = 0
        data = json.load(file)
        for line in data:
            pos = pos + line["pos"]
            neg = neg + line["neg"]
        if pos == 0 and neg == 0:
            score = 0
        elif neg == 0:
            score = float('inf')
        else:
            score = (pos/neg)
        all_scores[topic] = score
        all_scores_length[topic] = score * len(data)
        if topic in candidates:
            lengths[topic] = len(data)
            total_tweets = total_tweets + len(data)

outF = open('data/' + state + '/tumasjan/results/' + 'results.txt', 'w')
scores_sorted = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
for (topic, score) in scores_sorted:
    outF.write(topic + ' sentiment: ' + str(score))
    outF.write('\n')
outF.close()

outF = open('data/' + state + '/tumasjan/results/' + 'results_weighted.txt', 'w')
scores_length_sorted = sorted(all_scores_length.items(), key=lambda x: x[1], reverse=True)
for (topic, score) in scores_length_sorted:
    outF.write(topic + ' sentiment: ' + str(score))
    outF.write('\n')
outF.close()

outF = open('data/' + state + '/tumasjan/results/' + 'weights.txt', 'w')
lengths_sorted = sorted(lengths.items(), key=lambda x: x[1], reverse=True)
for (topic, score) in lengths_sorted:
    outF.write(topic + ' sentiment: ' + str(score/total_tweets))
    outF.write('\n')
outF.close()
