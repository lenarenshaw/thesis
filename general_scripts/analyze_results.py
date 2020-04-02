import csv
import math

P_VALUE = 0.05
states = ['iowa', 'newhampshire', 'nevada', 'southcarolina', 'alabama', 'arkansas', 'california', 'colorado', 'maine', 'massachusetts', 'minnesota', 'northcarolina', 'oklahoma', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'idaho', 'michigan', 'mississippi', 'missouri', 'northdakota', 'washington', 'arizona', 'florida', 'illinois']
test = 'oconnor'

winners_predicted_correctly = []
model_accepted = []

def gf(x):
    #Play with these values to adjust the error of the approximation.
    upper_bound=100.0
    resolution=1000000.0

    step=upper_bound/resolution

    val=0
    rolling_sum=0

    while val<=upper_bound:
        rolling_sum+=step*(val**(x-1)*2.7182818284590452353602874713526624977**(-val))
        val+=step

    return rolling_sum

def ilgf(s,z):
    val=0

    for k in range(0,100):
        val+=(((-1)**k)*z**(s+k))/(math.factorial(k)*(s+k))
    return val

def chisquarecdf(x,k):
    return 1-ilgf(k/2,x/2)/gf(k/2)

def chisquare(observed_values,expected_values):
    test_statistic=0

    for observed, expected in zip(observed_values, expected_values):
        test_statistic+=(float(observed)-float(expected))**2/float(expected)

    df=len(observed_values)-1

    return test_statistic, chisquarecdf(test_statistic,df)

for state in states:
    election_results = {}
    test_results = {}
    winner = ""
    winner_val = float('-inf')
    predicted_winner = ""
    predicted_winner_val = float('-inf')
    total_delegates = 0
    with open('data/' + state + '/election_results/' + state + '.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        line = next(reader, None)
        while line:
            votes = float(line['Total S.D.E.s*'].replace("\"", "").replace("\'", "").replace(",",""))
            candidate_name = line['Candidate'].split(" ")[0].lower()
            if votes > winner_val:
                winner = candidate_name
                winner_val = votes
            election_results[line['Candidate'].split(" ")[0].lower()] = votes
            total_delegates += votes
            line = next(reader, None)

    total_sentiment = 0
    with open('data/' + state + '/'+ test + '/results/results.txt', 'r') as file:
        for line in file:
            arr = line.split(" ")
            if arr[0] in election_results.keys():
                res = float(arr[-1])
                if res > predicted_winner_val:
                    predicted_winner = arr[0]
                    predicted_winner_val = res
                test_results[arr[0]] = float(arr[-1])
                total_sentiment += float(arr[-1])

    final_election_results = {}
    final_test_results = {}

    for candidate, score in election_results.items():
        if candidate in test_results.keys():
            final_test_results[candidate] = (test_results[candidate]/total_sentiment * 100) + 1
            final_election_results[candidate] = (score/total_delegates * 100) + 1

    a, b = chisquare(final_election_results.values(), final_test_results.values())

    print(state.capitalize())
    print("Predicted Winner", predicted_winner, "Actual Winner", winner)
    if predicted_winner == winner:
        winners_predicted_correctly.append(True)
    else:
        winners_predicted_correctly.append(False)
    print("Chi squared value:", a)
    if b < P_VALUE:
        print("Accept the model")
        model_accepted.append(True)
    else:
        print("Reject the model")
        model_accepted.append(False)

print("SUMMARY:")
print("Fraction of models accepted", round(model_accepted.count(True)/len(model_accepted), 5))
print("Fraction of winners correctly predicted", round(winners_predicted_correctly.count(True)/len(winners_predicted_correctly), 5))
