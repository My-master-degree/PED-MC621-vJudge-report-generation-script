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

#cookies session
cookies = {
        'Jax.Q': '',
        '_gid': '',
        'JSESSIONID': '',
        '_ga': ''
        }
#current contest files
contests = [
        'contests/MC621_MC821_08_11 - Virtual Judge.html',
        ]
#current username order
usernames = [
        'LuizAndia',
        'b164923',
        'hboschirolli',
        ];
#usernames list to present
usernames_to_present = [
        '<null>',
        'b164923',
        'hboschirolli',
        'LuizAndia',
]

usernames_order = {}
order = 1
for username in usernames:
    usernames_order[username] = order
    order += 1

#for each contest
for contest in contests:
    #setup
    f= open(contest,"r") 
    html =f.read()
    f.close()
    parsed_html = BeautifulSoup(html, from_encoding="utf-8")
    students = {}
    jsonData = json.loads(parsed_html.body.find('textarea', attrs = {'name' : "dataJson"}).text)
    contest_id = jsonData['id']
    n_problems = len(jsonData['problems'])
    end_contest_time = jsonData['end']
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
                'accepted': 0
                }
        for problem in range(n_problems):
            problem_letter = chr(ord('A') + problem)
            if VERBOSE:
                print("\t", problem_letter)
            #get request
            request = requests.get(
                    url = 'https://vjudge.net/status/data/',
                    params = {
                        'start': 0,
                        'length': 20,
                        'un': username,
                        'num': problem_letter,
                        'res': 1,
                        'language': '',
                        'inContest': True,
                        'contestId': contest_id
                        },
                    headers = {
                        'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9',
                        'cookie': "_ga="+cookies['_ga']+"; _gid="+cookies['_gid']+"; Jax.Q="+cookies['Jax.Q']+"; JSESSIONID="+cookies['JSESSIONID']+"; _gat=1",
                        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'x-requested-with': 'XMLHttpRequest'
                        }
                ).text
            response = json.loads(request)
            if len(response['data']) == 0:
                student['failed'] += 1
            else:
                valid = False
                for accepted in response['data']:
                    if accepted['time'] <= end_contest_time and accepted['userName'].lower() == student['user'].lower():
                        valid = True
                        break
                if valid:
                    student['accepted'] += 1
                else:
                    student['out_time'] += 1
        students[username] = student
    #get username rank
    rows = parsed_html.body.find('table', attrs={'id': 'contest-rank-table' }).tbody.find_all('tr')
    rank = 1
    for row in rows:
        if rank > 3:
            break;
        username = row.find('td', attrs={'class' : 'team'}).div.a.find(text=True, recursive=False).rstrip()
        if username in students:
            students[username]['rank'] = rank
            rank += 1
    #write csv
    with open(contest.split('/')[1] + ".csv", mode='w') as csv_file:
        fieldnames = ['user', 'accepted', 'out_time', 'rank', 'failed']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for username_to_present in usernames_to_present:
            row = {'user':username_to_present, 'accepted':0, 'out_time':0, 'rank':'', 'failed':0}
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
