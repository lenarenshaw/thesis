from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import sys

if len(sys.argv) != 2:
    print("Usage: python3 vader_sentiment.py <state-name>")
state = sys.argv[1]

keywords = ['biden', 'gabbard', 'sanders']

all_data = {}
analyzer = SentimentIntensityAnalyzer()

for topic in keywords:
    with open('data/' + state + '/raw_tweets/' + topic + '.txt', 'r') as file:
        lines = file.readlines()
        results = []
        for line in lines:
            vs = analyzer.polarity_scores(line)
            results.append(vs)
        all_data[topic] = results

for topic in keywords:
    outF = open('data/' + state + '/tumasjan/' + topic + '_polarity.json', 'w')
    json.dump(all_data[topic], outF)
