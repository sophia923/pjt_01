import requests 
import json
import csv
# from datetime import datetime, timedelta
from decouple import config
from pprint import pprint


result = []
with open('movies.csv', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)


    for row in reader:
       code = row.get('peopleNm')
       result.append(code)
# print(type(result)) 
# #리스트로 뽑음



results = {}
for code_new in result:
    key = config('S_KEY')
    
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?peopleNm={code_new}&key={key}&itemPerPage=100'
    api_data = requests.get(url).json() 

    

    movies = api_data.get('peopleListResult').get('peopleList')[0]
    # pprint(movies) 여기서 프린트를 해서 감독 배우 이런 분류가 있다는 것을 알고 if 절이 들어가야 한다는 것을 깨달음!
    code_new = movies.get('peopleCd')
    rep_rol = movies.get('repRoleNm')
# pprint(code_new)
    if code_new not in results and rep_rol == '감독':
        results[code_new] = {
            'peopleCd' : movies.get('peopleCd'),
            'peopleNm' : movies.get('peopleNm'),
            'repRoleNm' : movies.get('repRoleNm'),
            'filmoNames' : movies.get('filmoNames')
            }
    else:
        None   
pprint(results) 

with open('director.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['peopleCd', 'peopleNm', 'repRoleNm', 'filmoNames']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in results.values():
        writer.writerow(value)
