import csv
import math
from scipy.stats import pearsonr
import numpy as np

P_VALUE = 0.05
states = ['iowa', 'newhampshire', 'nevada', 'southcarolina', 'alabama', 'arkansas', 'california', 'colorado', 'maine', 'massachusetts', 'minnesota', 'northcarolina', 'oklahoma', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'idaho', 'michigan', 'mississippi', 'missouri','washington', 'arizona', 'florida', 'illinois']
test = 'oconnor'

winners_predicted_correctly = []
model_accepted = []
correlations = []

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
    try:
        return 1-ilgf(k/2,x/2)/gf(k/2)
    except OverflowError:
        print("Could not calculate gf")
        return(P_VALUE)
    except ZeroDivisionError:
        print("Could not calculate gf")
        return(P_VALUE)

def chisquare(observed_values,expected_values):
    test_statistic=0

    for observed, expected in zip(observed_values, expected_values):
        test_statistic+=(float(observed)-float(expected))**2/float(expected)

    df=len(observed_values)-1

    return test_statistic, chisquarecdf(test_statistic,df)

for state in states:
    poll_results = []
    sentiment_results = []

    with open('data/' + state + '/oconnor/poll-results.csv', 'r', encoding='utf-8-sig') as file:
        sums = None
        first_line = True
        l = 0
        for line in file:
            if not first_line:
                if sums is None:
                    sums = np.asarray(line.split(",")[1:])
                    sums = sums.astype(np.float)
                else:
                    tmp = np.asarray(line.split(",")[1:])
                    tmp = tmp.astype(np.float)
                    sums = sums + tmp
            l = l + 1
            first_line = False
        poll_results = sums/l


    with open('data/' + state + '/oconnor/dated-sentiment-results.csv', 'r', encoding='utf-8-sig') as file:
        sums = None
        first_line = True
        l = 0
        for line in file:
            if not first_line:
                if sums is None:
                    tmp = np.asarray(line.split(",")[1:])
                    tmp = tmp.astype(np.float)
                    sums = tmp / np.linalg.norm(tmp)
                else:
                    tmp = np.asarray(line.split(",")[1:])
                    tmp = tmp.astype(np.float)
                    sums = sums + tmp
            l = l + 1
            first_line = False
        sentiment_results = sums/l

    x = 0
    delete = []
    for item in poll_results:
        if item == 0 and sentiment_results[x] == 0:
            delete.append(x)
        x = x + 1

    poll_results = np.delete(poll_results, delete)
    sentiment_results = np.delete(sentiment_results, delete)

    poll_total = np.sum(poll_results)
    poll_results = poll_results / poll_total

    sentiment_total = np.sum(sentiment_results)
    sentiment_results = sentiment_results / sentiment_total

    a, b = chisquare(poll_results + 1, sentiment_results + 1)

    print(state.capitalize())

    print("Chi squared value:", a)
    if b < P_VALUE:
        print("Accept the model")
        model_accepted.append(True)
    else:
        print("Reject the model")
        model_accepted.append(False)
    # calculate Pearson's correlation
    corr, _ = pearsonr(poll_results + 1, sentiment_results + 1)
    print('Pearsons correlation: %.3f' % corr)
    correlations.append(corr)

print("SUMMARY:")
print("Fraction of models accepted", round(model_accepted.count(True)/len(model_accepted), 5))
print("Average correlation", round(sum(correlations)/len(correlations), 5))
