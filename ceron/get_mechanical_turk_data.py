import json
import csv
from langdetect import detect
import random

states = ['iowa', 'newhampshire', 'nevada', 'southcarolina', 'alabama', 'arkansas', 'california', 'colorado', 'maine', 'massachusetts', 'minnesota', 'northcarolina', 'oklahoma', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'idaho', 'michigan', 'mississippi', 'missouri', 'northdakota', 'washington', 'arizona', 'florida', 'illinois']
num_tweets_per_state = int((50/0.04) / len(states)) / 3
all_tweets = []

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

for state in states:
    state_tweets = []
    max_val = 0
    with open('data/' + state + '/ceron/'+ state +'-ceron-training.json') as json_file:
        data = json.load(json_file)
        random.shuffle(data)
        for tweet in data:
            if max_val > num_tweets_per_state:
                break
            text = tweet['text']
            text = text.replace('\n', ' ')
            try:
                if text != "" and detect(text) == 'en' and text and is_ascii(text):
                    state_tweets.append([text, state])
                    max_val += 1
            except:
                print("Error:", text)

    with open('data/ceron/mechanical-turk-training-data-' + state + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['text', 'state'])
        print("Writing out " + str(max_val) + " tweets to " + 'data/ceron/mechanical-turk-training-data-' + state)
        for line in state_tweets[0:max_val]:
            all_tweets.append(line)
            writer.writerow(line)

with open('data/ceron/mechanical-turk-training-data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['text', 'state'])
    for line in all_tweets:
        writer.writerow(line)
