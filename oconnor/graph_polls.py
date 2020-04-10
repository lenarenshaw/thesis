import pandas as pd
import matplotlib.pyplot as plt

state = 'iowa'

polls = pd.read_csv('data/' + state + '/oconnor/poll-results.csv')
sentiment = pd.read_csv('data/' + state + '/oconnor/dated-sentiment-results.csv')

polls_drop_indices = []
sentiment_drop_indices = []

for index, row in polls.iterrows():
    if row['date'] not in list(sentiment['date']):
        polls_drop_indices.append(index)

for index, row in sentiment.iterrows():
    if row['date'] not in list(polls['date']):
        sentiment_drop_indices.append(index)

polls = polls.drop(polls_drop_indices)
sentiment = sentiment.drop(sentiment_drop_indices)

polls = polls.rename(columns={"bennet": "bennet1" ,'biden': 'biden1','bloomberg':'bloomberg1',
'buttigieg':'buttigieg1','gabbard':'gabbard1','klobuchar':'klobuchar1','patrick':'patrick1',
'sanders':'sanders1','steyer':'steyer1','warren':'warren1','yang':'yang1'})

polls = polls.set_index('date')
sentiment = sentiment.set_index('date')

polls = polls.div(polls.sum(axis=1), axis=0).fillna(0)
sentiment = sentiment.div(sentiment.sum(axis=1), axis=0).fillna(0)

results = pd.concat([sentiment, polls], axis=1)

biden = pd.DataFrame({'Biden Polls': polls['biden1'], 'Biden Sentiment': sentiment['biden'], 'Sanders Polls': polls['sanders1'], 'Sanders Sentiment': sentiment['sanders'], 'Buttigieg Polls': polls['buttigieg1'], 'Buttigieg Sentiment': sentiment['buttigieg']}, index=results.index)

lines = biden.plot.line(color=['#a10d00', '#ff5f4f', '#0e79eb', '#0020d6', "#00a344", "#00ff6a"])

plt.show()
