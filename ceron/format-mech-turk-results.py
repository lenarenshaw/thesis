import csv

all_data = {}

with open('data/ceron/mech-turk-results.csv') as csv_file:
    csv_file_reader = csv.DictReader(csv_file)
    for row in csv_file_reader:
        if row["Input.state"] not in all_data.keys():
            all_data[row["Input.state"]] = {}
        dct = all_data[row["Input.state"]]
        if row["Input.text"] not in dct.keys():
            dct[row["Input.text"]] = []
        lst = dct[row["Input.text"]]
        lst.append(row["Answer.sentiment.label"])
        dct[row["Input.text"]] = lst
        all_data["Input.state"] = dct

with open('data/ceron/training.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['tweet', 'sentiment'])
    for state, dct in all_data.items():
        for tweet, sent_list in dct.items():
            writer.writerow([tweet, max(set(sent_list), key=sent_list.count)])
