try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from pprint import pprint
import csv
import datetime
import requests 
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
#for each contest
for contest in contests:
    #setup
    f= open(contest,"r") 
    html =f.read()
    f.close()
    parsed_html = BeautifulSoup(html, from_encoding="utf-8")
    students = [];    
    #iterate over students
    trs = parsed_html.body.find('table', attrs={'id': 'contest-rank-table' }).tbody.find_all('tr')
    th = 1
    for tr in trs:
        student = {'failed': 0, 'rank': th, 'out_time': 0}
        contest_id = tr.get('c')
        user_id = tr.get('u')        
        if contest_id == None:
            print(tr)
            exit()
        tds = tr.find_all('td')        
        problem_letter = 'A'
        for td in tds:
            # get name
            if td.div != None and td.div.a != None: 
                student['user'] = td.div.a.find(text=True, recursive=False).rstrip()
            # get accepted question
            classes = td.get('class')
            if 'solved' in classes:
                student['accepteds'] = td.a.text
            #if 'accepted' in classes and datetime.datetime.strptime(td.find(text=True, recursive=False), '%H:%M:%S').time() > ending_timestamp:
            if 'failed' in classes:
                submissions_page = BeautifulSoup(requests.get(url = 'https://vjudge.net/contest/teamProblemStatus/'+contest_id+'?uid='+user_id+'&num='+problem_letter+'&afterContest=true', params = {}).text, from_encoding="utf-8")
                if submissions_page.body.table.tbody.find('tr', attrs = {'class':'accepted'}) == None:
                    student['failed'] += 1
                else:
                    student['out_time'] += 1
            if 'prob' in classes:
                problem_letter = chr(ord(problem_letter) + 1)

        if 'user' in student:
            students.append(student)
            th += 1
    #sort values
    students.sort(key= lambda val: usernames_order[val['user']] if val['user'] in usernames_order else 10000000)
    #write csv
    with open(contest.split('/')[1] + ".csv", mode='w') as csv_file:
        fieldnames = ['user', 'accepteds', 'failed', 'rank', 'out_time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow(student)
    break
