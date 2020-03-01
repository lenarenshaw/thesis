import json
import sys

if len(sys.argv) != 2:
    print("Usage: python3 get_test_and_train_data.py <state-name>")
state = sys.argv[1]

keywords = ['bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang', 'democrat', 'dem', 'caucus', 'primary']

# CREATE TRAINING DATA
all_training_data = {}
processed_training_data = {}
for topic in keywords:
    all_training_data[topic] = []
    processed_training_data[topic] = []

for topic in keywords:
    with open('data/' + state + '/ceron/' + topic + "-training-data.txt_auto_anns/subjclueslen1polar", 'r') as file:
        for line in file:
            arr = line.split()
            chars = arr[1].split(",")
            sentiment = arr[4].split("\"")[1]
            chars.append(sentiment)
            lst = all_training_data[topic]
            lst.append(chars)
            all_training_data[topic] = lst

for topic in keywords:
    with open('data/' + state + '/ceron/' + topic + "-training-data.txt") as file:
        data = file.read().replace('\n', ' ')
        for char_tuple in all_training_data[topic]:
            lst = processed_training_data[topic]
            lst.append((data[int(char_tuple[0]) - 1:int(char_tuple[1])].replace("\'", "").replace("“", "").replace("\"", ""), char_tuple[2]))
            processed_training_data[topic] = lst


outF = open('data/' + state + '/ceron/all-training-data.csv', 'w')
outF.write('Word,Polarity\n')
s = set()
for topic in keywords:
    for tuple in processed_training_data[topic]:
        if (tuple[0].strip() not in s):
            s.add(tuple[0].strip())
            outF.write(tuple[0].strip())
            outF.write(",")
            outF.write(tuple[1].strip())
            outF.write('\n')
outF.close()

# FORMAT TESTING DATA
all_testing_data = {}
processed_testing_data = {}
for topic in keywords:
    all_testing_data[topic] = []
    processed_testing_data[topic] = []

for topic in keywords:
    with open('data/' + state + '/oconnor/' + topic + ".txt_auto_anns/subjclueslen1polar", 'r') as file:
        for line in file:
            arr = line.split()
            chars = arr[1].split(",")
            sentiment = arr[4].split("\"")[1]
            chars.append(sentiment)
            lst = all_testing_data[topic]
            lst.append(chars)
            all_testing_data[topic] = lst

for topic in keywords:
    with open('data/' + state + '/raw_tweets/' + topic + ".txt") as file:
        data = file.read().replace('\n', ' ')
        for char_tuple in all_testing_data[topic]:
            lst = processed_testing_data[topic]
            lst.append((data[int(char_tuple[0]) - 1:int(char_tuple[1])].replace("\'", "").replace("“", "").replace("\"", ""), char_tuple[2]))
            processed_testing_data[topic] = lst

for topic in keywords:
    outF = open('data/' + state + '/ceron/' + topic + '_testing_data.csv', 'w')
    outF.write('Word,Polarity\n')
    s = set()
    for tuple in processed_testing_data[topic]:
        if (tuple[0].strip() not in s):
            s.add(tuple[0].strip())
            outF.write(tuple[0].strip())
            outF.write(",")
            outF.write(tuple[1].strip())
            outF.write('\n')
    outF.close()
