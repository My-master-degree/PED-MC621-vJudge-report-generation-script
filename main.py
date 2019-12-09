try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from pprint import pprint
import csv
import datetime
import requests 
import json
#current contest files
contests = [
        'contests/MC621_MC821_01_11 - Virtual Judge.html',  
        'contests/MC621_MC821_16_08 - Virtual Judge.html',
        'contests/MC621_MC821_02_08 - Virtual Judge.html',
        'contests/MC621_MC821_18_10 - Virtual Judge.html',
        'contests/MC621_MC821_04_10 - Virtual Judge.html',
        'contests/MC621_MC821_20_09 - Virtual Judge.html',
        'contests/MC621_MC821_06_09 - Virtual Judge.html',
        'contests/MC621_MC821_22_11 - Virtual Judge.html',
        'contests/MC621_MC821_08_11 - Virtual Judge.html',
        'contests/MC621_MC821_23_08 - Virtual Judge.html',
        'contests/MC621_MC821_11_10 - Virtual Judge.html',
        'contests/MC621_MC821_25_10 - Virtual Judge.html',
        'contests/MC621_MC821_13_09 - Virtual Judge.html',
        'contests/MC621_MC821_27_09 - Virtual Judge.html',
        'contests/MC621_MC821_15_11 - Virtual Judge.html',
        'contests/MC621_MC821_30_08 - Virtual Judge.html'
        ]
#current sutends username order
usernames = [
        'LuizAndia',
        'andregoncalves',
        'FelipeEmos',
        'ggavena',
        'wmartins',
        'FerParedes',
        'dominguilherme',
        'guilhermehhs',
        'anarequena',
        'b164923',
        'krautz',
        'AnaClaraZS',
        'brunoaf',
        'guilhermetiaki',
        'danieloliveira',
        'hboschirolli',
        'ericoimf',
        'Leandroafm21',
        'gfrancioli',
        'gabrielmsato',
        'giocoutinho26',
        'mihmosa',
        'luizguilherme',
        'Gustavo_Salibi',
        'natrodrigues',
        'joaopm',
        'victormaruca',
        'MarcoAurelio',
        'mjoaquim',
        'barney_san',
        'turing_burro',
        'tiagodepalves',
        'VitoriaDMP',
        'erickkn',
        'gabrielsantosrv',
        'VBS',
        'joaoguilhermeas',
        'JoaoFlores',
        'lumagabinov',
        'maviles',
        'Pupo',
        'pedromorelli96',
        'vitormosso',
        'Fatayer',
        'AlvaroMarques',
        'beatrizazanha',
        'Fingerman',
        'Ieremies',
        'Zanez',
        'luizgustavo09',
        ];
usernames_order = {}
order = 1
for username in usernames:
    usernames_order[username] = order
    order += 1
#usernames list to present
usernames_to_present = [
        'LuizAndia',
        'andregoncalves',
        'FelipeEmos',
        'ggavena',
        'wmartins',
        'FerParedes',
        'dominguilherme',
        'guilhermehhs',
        'anarequena',
        'b164923',
        '<insira username vjudge aqui>',
        'krautz',
        'AnaClaraZS',
        '<insira username vjudge aqui>',
        'brunoaf',
        'guilhermetiaki',
        'danieloliveira',
        'hboschirolli',
        '<insira username vjudge aqui>',
        'ericoimf',
        'Leandroafm21',
        'gfrancioli',
        'gabrielmsato',
        '<insira username vjudge aqui>',
        'giocoutinho26',
        'mihmosa',
        'luizguilherme',
        'Gustavo_Salibi',
        'natrodrigues',
        'joaopm',
        '<insira username vjudge aqui>',
        'victormaruca',
        '<insira username vjudge aqui>',
        '<insira username vjudge aqui>',
        '<insira username vjudge aqui>',
        '<insira username vjudge aqui>',
        'MarcoAurelio',
        '<insira username vjudge aqui>',
        'mjoaquim',
        'barney_san',
        'turing_burro',
        'tiagodepalves',
        '<insira username vjudge aqui>',
        'VitoriaDMP',
        '<insira username vjudge aqui>',
        'erickkn',
        'gabrielsantosrv',
        '<insira username vjudge aqui>',
        'VBS',
        'joaoguilhermeas',
'JoaoFlores',
       'lumagabinov',
       'maviles',
       'Pupo',
       'pedromorelli96',
       'vitormosso',
       'Fatayer',
       'AlvaroMarques',
       'beatrizazanha',
       'Fingerman',
       'Ieremies',
       'Zanez',
       '<insira username vjudge aqui>',
       'luizgustavo09',
       '<insira username vjudge aqui>',
       '<insira username vjudge aqui>',
       '<insira username vjudge aqui>'
]

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
        student = {
                'user': username,
                'failed': 0, 
                'rank': 0, 
                'out_time': 0, 
                'accepted': 0
                }
        for problem in range(n_problems):
            problem_letter = chr(ord('A') + problem)
            #post request
            columns = []
            for i in range(9):
                columns.append(
                    {
                        'data': i,
                        'name': '',
                        'searchable': True,
                        'orderable': False,
                        'search': {
                            'value' : '',
                            'regex': False
                        },
                    }
                )
            request = requests.post(
                    url = 'https://vjudge.net/status/data/', 
                    params = {
                        'columns' : columns, 
                        'start': 0,
                        'length': 20,
                        'search': {
                            'value': '',
                            'regex': False
                            },
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
                        'cookie': '_ga=GA1.2.990671163.1570647124; _gid=GA1.2.52825728.1575479159; Jax.Q=mc521721_2019|Y9GT8VNDVOBDEPC9707ZV77OF4RCY4; JSESSIONID=27A6644053B7B0F22933CBC4DC2AE9E4; _gat=1',
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
                    if accepted['time'] <= end_contest_time:
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
                        row['rank'] = 'PRIMEIRO'
                    elif row['rank'] == 2:
                        row['rank'] = 'SEGUNDO'
                    elif row['rank'] == 3:
                        row['rank'] = 'TERCEIRO'
                    else:
                        row['rank'] = ''
                    break
            writer.writerow(row)
