from datetime import date, timedelta
import csv

states = ['iowa', 'newhampshire', 'nevada', 'southcarolina', 'alabama', 'arkansas', 'california', 'colorado', 'maine', 'massachusetts', 'minnesota', 'northcarolina', 'oklahoma', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'idaho', 'michigan', 'mississippi', 'missouri', 'washington', 'arizona', 'florida', 'illinois']

candidate_exits = {'bennet':date(2020, 2, 11),
    'biden': date(2021, 1, 1), #not out
    'bloomberg': date(2020, 3, 4),
    'buttigieg': date(2020, 3, 1),
    'gabbard': date(2020, 3, 19),
    'klobuchar': date(2020, 3, 2),
    'patrick': date(2020, 2, 12),
    'sanders':date(2021, 1, 1), #not out
    'steyer': date(2020, 2, 9),
    'warren': date(2020, 3, 5),
    'yang': date(2020, 2, 11)}

state_elections = {
    #year, month, day
    'iowa': date(2020, 2, 3),
    'newhampshire': date(2020, 2, 11),
    'nevada': date(2020, 2, 22),
    'southcarolina': date(2020, 2, 29),
    'alabama': date(2020, 3, 3),
    'americansamoa': date(2020, 3, 3),
    'arkansas': date(2020, 3, 3),
    'california': date(2020, 3, 3),
    'colorado': date(2020, 3, 3),
    'maine': date(2020, 3, 3),
    'massachusetts': date(2020, 3, 3),
    'minnesota': date(2020, 3, 3),
    'northcarolina': date(2020, 3, 3),
    'oklahoma': date(2020, 3, 3),
    'tennessee': date(2020, 3, 3),
    'texas': date(2020, 3, 3),
    'utah': date(2020, 3, 3),
    'vermont': date(2020, 3, 3),
    'virginia': date(2020, 3, 3),
    'idaho': date(2020, 3, 10),
    'michigan': date(2020, 3, 10),
    'mississippi': date(2020, 3, 10),
    'missouri': date(2020, 3, 10),
    'northdakota': date(2020, 3, 10),
    'washington': date(2020, 3, 10),
    'guam': date(2020, 3, 14),
    'northernmariana': date(2020, 3, 14),
    'arizona': date(2020, 3, 17),
    'florida': date(2020, 3, 17),
    'illinois': date(2020, 3, 17)
}

for state in states:
    print(state)
    with open('data/' + state + '/oconnor/' + state + '-polls.csv', 'r', encoding='utf-8-sig') as file:
        dates = {}
        reader = csv.DictReader(file)
        poll_candidates = reader.fieldnames
        line = next(reader, None)
        year = 2020
        was_prev_dec = False
        while line:
            for candidate in candidate_exits.keys():
                if candidate_exits[candidate] >= state_elections[state] and candidate.capitalize() in poll_candidates:
                    # we should use that candidate
                    if line['Date'] != '--':
                        arr = line['Date'].split(' - ')
                        if arr[0].split('/')[0] == '12' and not was_prev_dec:
                            year = year - 1
                            was_prev_dec = True
                        if arr[0].split('/')[0] != '12' and was_prev_dec:
                            was_prev_dec = False

                        sdate = date(year, int(arr[0].split('/')[0]), int(arr[0].split('/')[1]))   # start date
                        edate = date(year, int(arr[1].split('/')[0]), int(arr[1].split('/')[1]))  # end date

                        delta = edate - sdate # as timedelta
                        for i in range(delta.days + 1):
                            day = sdate + timedelta(days=i)
                            if day not in dates.keys():
                                dates[day] = {}
                            dct = dates[day]
                            if candidate not in dct.keys():
                                if line[candidate.capitalize()] != '--' and line[candidate.capitalize()] != '':
                                    dct[candidate] = (float(line[candidate.capitalize()]), 1)
                            else:
                                if line[candidate.capitalize()] != '--' and line[candidate.capitalize()] != '':
                                    so_far, num = dct[candidate]
                                    dct[candidate] = (float(line[candidate.capitalize()]) + so_far, num + 1)
                            dates[day] = dct

            line = next(reader, None)

    with open('data/' + state + '/oconnor/poll-results.csv', 'w') as csv_file:
        three_weeks_prior = state_elections[state] - timedelta(days=21)
        writer = csv.writer(csv_file, delimiter=',')
        header = ['date']
        for candidate in candidate_exits.keys():
            header.append(candidate)
        writer.writerow(header)
        for i in range(21):
            day = three_weeks_prior + timedelta(days=i)
            if day in dates.keys():
                results = dates[day]
                lst = [day]
                for candidate in candidate_exits.keys():
                    if candidate in results.keys():
                        score, num = results[candidate]
                        lst.append(score/num)
                    else:
                        lst.append(0)
                writer.writerow(lst)
