import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

def csv_to_json(filename):
    data = pd.read_csv(filename, header=0)
    return data.to_dict('records')

def main():
    client = MongoClient('mongodb+srv://lenarenshaw:qwerty12@renshawthesis2-spgqz.mongodb.net/test?retryWrites=true&w=majority')

    politics_db = client['politics_db']
    anes_voter_survey = politics_db['anes_voter_survey']

    # results = csv_to_json('anes_timeseries_cdf_dta/anes_timeseries_cdf.csv')
    # anes_voter_survey.insert_many(results)

if __name__ == "__main__":
    main()
