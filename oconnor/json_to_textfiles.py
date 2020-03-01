import json
import sys

if len(sys.argv) != 2:
    print("Usage: python3 json_to_textfiles.py <state-name>")
state = sys.argv[1]

keywords = ['bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang', 'democrat', 'dem', 'caucus', 'primary']

all_tweets = {}
for topic in keywords:
    all_tweets[topic] = []

with open('data/' + state + '/raw_tweets/'+ state +'.json') as json_file:
    data = json.load(json_file)
    for tweet in data:
        text = tweet['text']
        text = text.replace('\n', ' ')
        text = text.replace('.', '')
        text = text + '.'
        for topic in keywords:
            if topic in text:
                lst = all_tweets[topic]
                lst.append(text)
                all_tweets[topic] = lst

for topic in keywords:
    outF = open('data/' + state + '/raw_tweets/' + topic + '.txt', 'w')
    for line in all_tweets[topic]:
        outF.write(line)
        outF.write('\n')
    outF.close()

outF = open('oconnor/opinionfinderv2.0/' + state + '.doclist', 'w')
for topic in keywords:
    outF.write('../../data/' + state + '/raw_tweets/' + topic + '.txt')
    outF.write('\n')
outF.close()
