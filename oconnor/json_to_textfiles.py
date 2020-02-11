import json

# state = 'iowa'
state = 'newhampshire'

keywords = ['bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang', 'democrat', 'dem', 'caucus', 'primary']

all_tweets = {}
for topic in keywords:
    all_tweets[topic] = []

with open('../data/' + state + '/'+ state +'.json') as json_file:
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
    outF = open('../data/' + state + '/oconnor/' + topic + '.txt', 'w')
    for line in all_tweets[topic]:
        outF.write(line)
        outF.write('\n')
    outF.close()
