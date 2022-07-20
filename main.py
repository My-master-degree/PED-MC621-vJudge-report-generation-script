try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from pprint import pprint
import csv
import datetime
import requests 
import json
import sys

VERBOSE = False

#get command line args
n_args = len(sys.argv)
for i in range(1, n_args):
    print(sys.argv[i], )
    if sys.argv[i] == "--verbose":
        VERBOSE = True

contests_ids = [
    479096,
    479242,
    480758,
    481176,
    481292,
    487571,
    488410,
    491161,
    491162,
    496398,
    496399,
    497394,
    498296,
    499186,
]

#current username order
usernames = [
    'hermes_shimizu',
    'DanielCoimbra',
    'pirapombo',
    'GiovanniCDB',
    'jpsousa',
    'Thcerbla',
    'LucasOli',
    'lumalombello',
    'Dantas',
    'ramos',
    'hiriluk',
    'humanolaranja',
    'guilhermeShima',
    'jhonatas',
    'joaoguilherme',
    'j199944',
    'Lucas_Lopes',
    'mcnunes',
    'MatheusOliveira',
    'maurilio',
    'oozaku',
    'AndreLuisRG',
    'Dorival',
    'FelipePM01',
    'gdseabra',
    'GeorgeGGJ',
    'kaiotakuma',
    'LucasFarias',
    'mariliacss',
    'MateusOlivi',
    'MylenaRoberta',
    'Pedro_Hori',
    'Desnord',
    'FabioVillar',
    'fer20comp',
    'f234589',
    'Vinidamasceno',
    'casotavo',
    'marcoscunharosa',
    'mferraz',
    'mugomes',
    'thaina',
    'VPietrobom',
    'fernandomarques',
    'PhilipeMS',
    'caiopetruccirosa',
    'joaodm423',
    'lucasfrancisco',
    'Savitsky',
    'CristianoSampaio',
    'Cl3T0',
    'igorfrade',
    'ccarneiro',
    'gmarques.daniel',
    'victormaruca',
    'BassaniZ',
    'QSRafael',
    'Eric_V',
    'luizgustavo09',
    'notGut',
];
#usernames list to present
usernames_to_present = [
    '',
    '',
    'hermes_shimizu',
    'DanielCoimbra',
    '',
    'pirapombo',
    'GiovanniCDB',
    '',
    'jpsousa',
    'Thcerbla',
    '',
    '',
    'LucasOli',
    'lumalombello',
    '',
    'Dantas',
    '',
    'ramos',
    'hiriluk',
    'humanolaranja',
    'guilhermeShima',
    'jhonatas',
    'joaoguilherme',
    'j199944',
    'Lucas_Lopes',
    'mcnunes',
    'MatheusOliveira',
    'maurilio',
    'oozaku',
    'AndreLuisRG',
    'Dorival',
    'FelipePM01',
    'gdseabra',
    'GeorgeGGJ',
    'kaiotakuma',
    'LucasFarias',
    'mariliacss',
    'MateusOlivi',
    'MylenaRoberta',
    'Pedro_Hori',
    'Desnord',
    'FabioVillar',
    'fer20comp',
    'f234589',
    'Vinidamasceno',
    'casotavo',
    '',
    'marcoscunharosa',
    'mferraz',
    'mugomes',
    '',
    'thaina',
    'VPietrobom',
    '',
    'fernandomarques',
    'PhilipeMS',
    'caiopetruccirosa',
    'joaodm423',
    'lucasfrancisco',
    'Savitsky',
    'CristianoSampaio',
    'Cl3T0',
    'igorfrade',
    '',
    'ccarneiro',
    'gmarques.daniel',
    'victormaruca',
    'BassaniZ',
    '',
    'QSRafael',
    'Eric_V',
    '',
    '',
    '',
    '',
    'luizgustavo09',
    '',
    '',
    'notGut',
]

usernames_order = {}
order = 1
for username in usernames:
    usernames_order[username] = order
    order += 1

#for each contest
for contest_id in contests_ids:
    if verbose:
        print("contest_id: " + str(contest_id))
    #setup
    request = requests.get(
        url = 'https://vjudge.net/contest/'+str(contest_id),
    ).text
    parsed_html = BeautifulSoup(request, from_encoding="utf-8")
    students = {}
    jsonData = json.loads(parsed_html.body.find('textarea', attrs = {'name' : "dataJson"}).text)
    n_problems = len(jsonData['problems'])
    begin_contest_time = jsonData['begin']
    end_contest_time = jsonData['end']
    contest = jsonData['title']
    if VERBOSE:
        print(contest)
    #iterate over usernames
    for username in usernames:
        if VERBOSE:
            print("\t", username)
        student = {
                'user': username,
                'failed': 0, 
                'rank': 0, 
                'out_time': 0, 
                'accepted': 0,
                'penalty': 0,
                }
        for problem in range(n_problems):
            problem_letter = chr(ord('A') + problem)
            if VERBOSE:
                print("\t\t", problem_letter)
            solved = False
            solving_time = end_contest_time + 1
            start = 0;
            while True:
                request = requests.get(
                        url = 'https://vjudge.net/status/data/',
                        params = {
                            'start': start,
                            'length': 20,
                            'un': username,
                            'num': problem_letter,
                            },
                    ).text
                response = json.loads(request)
                for data in response['data']:
                    if data['statusType'] == 0 and data['userName'].lower() == student['user'].lower() and data['contestId'] == contest_id:
                        solved = True
                        solving_time = data['time']
                        break
                if len(response['data']) == 20:
                    start += 20
                else:
                    break
            if solved:
                if solving_time <= end_contest_time:
                    student['accepted'] += 1
                else:
                    student['out_time'] += 1
            else:
                student['failed'] += 1
            # compute penalty
            if solved:
                start = 0;
                while True:
                    request = requests.get(
                            url = 'https://vjudge.net/status/data/',
                            params = {
                                'start': start,
                                'length': 20,
                                'un': username,
                                'num': problem_letter,
                                },
                        ).text
                    response = json.loads(request)
                    for data in response['data']:
                        if data['userName'].lower() == student['user'].lower() and data['contestId'] == contest_id:
                            if data['statusType'] == 0:
                                student['penalty'] += round((data['time']-begin_contest_time)/60000)
                            else:
                                student['penalty'] += 20
                    if len(response['data']) == 20:
                        start += 20
                    else:
                        break
        students[username] = student
    #get username rank
    for username in usernames:
        students[username]['rank'] = sum((student['accepted'] > students[username]['accepted'] or (student['accepted'] == students[username]['accepted'] and student['penalty'] < students[username]['penalty'])) for student in students.values()) + 1
    with open(contest.split('/')[1] + ".csv", mode='w') as csv_file:
        fieldnames = ['user', 'accepted', 'out_time', 'rank', 'failed', 'penalty']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for username_to_present in usernames_to_present:
            row = {'user':username_to_present, 'accepted':0, 'out_time':0, 'rank':'', 'failed':0, 'penalty':0}
            for username in students:
                if username == username_to_present:
                    row = students[username]
                    if row['rank'] == 1:
                        row['rank'] = 'FIRST'
                    elif row['rank'] == 2:
                        row['rank'] = 'SECOND'
                    elif row['rank'] == 3:
                        row['rank'] = 'THIRD'
                    else:
                        row['rank'] = ''
                    break
            writer.writerow(row)
