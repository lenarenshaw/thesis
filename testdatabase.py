import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

def main():
    client = MongoClient('mongodb+srv://lenarenshaw:qwerty12@renshawthesis2-spgqz.mongodb.net/test?retryWrites=true&w=majority')

    test_db = client['test_db']
    test_collection = test_db['test_collection']
    lst = test_collection.find()
    for i in lst:
        print(i)

if __name__ == "__main__":
    main()
