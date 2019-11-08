import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

def main():
    client = MongoClient('mongodb+srv://lenarenshaw:qwerty12@renshawthesis2-spgqz.mongodb.net/test?retryWrites=true&w=majority')

    politics_db = client['politics_db']
    presidents_elected = politics_db['presidents_elected']
    lst = presidents_elected.find()
    for i in lst:
        print(i)

    def csv_to_json(filename):
        data = pd.read_csv(filename, header=0)
        return data.to_dict('records')

    results = csv_to_json('1976-2016-president.csv')
    presidents_elected.insert_many(results)

if __name__ == "__main__":
    main()
