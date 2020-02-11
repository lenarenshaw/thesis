state = 'newhampshire'
keywords = ['bennet', 'biden', 'bloomberg', 'buttigieg', 'gabbard', 'klobuchar', 'patrick', 'sanders', 'steyer', 'warren', 'yang', 'democrat', 'dem', 'caucus', 'primary']

all_scores = {}
all_scores_length = {}
for topic in keywords:
    all_scores[topic] = 0
    all_scores_length[topic] = 0

for topic in keywords:
    file = open('../data/' + state + '/oconnor/' + topic + '.txt')
    l = 0
    for line in file:
        l += 1
    file = open('../data/' + state + '/oconnor/' + topic + '.txt_auto_anns/subjcluesSentenceClassifiersOpinionFinderJune06', 'r')
    pos = 0
    neg = 0
    for line in file:
        arr = line.split(' ')
        type = arr[-1].split('\"')[1]
        if type == 'strongpos':
            pos += 2
        elif type == 'weakpos':
            pos += 1
        elif type == 'strongneg':
            neg += 2
        elif type == 'weakneg':
            neg += 1
    if pos == 0 and neg == 0:
        score = 0
    elif neg == 0:
        score = float('inf')
    else:
        score = (pos/neg)
    # print(topic + ': ' + str(pos) + '/' + str(neg) + '*' + str(l) + ' = ' + str(score))
    all_scores[topic] = score
    all_scores_length[topic] = score * l

outF = open(state + '_results.txt', 'w')
scores_sorted = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
for (topic, score) in scores_sorted:
    outF.write(topic + ' sentiment: ' + str(score))
    outF.write('\n')
outF.close()

outF = open(state + '_results_weighted.txt', 'w')
scores_length_sorted = sorted(all_scores_length.items(), key=lambda x: x[1], reverse=True)
for (topic, score) in scores_length_sorted:
    outF.write(topic + ' sentiment: ' + str(score))
    outF.write('\n')
outF.close()
