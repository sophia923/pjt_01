# 위에서 수집한 영화 대표코드를 활용하여 상세 정보를 수집합니다. 해당 데이터는 향후 영화평점서비스에서 영화 정보로 활용될 것입니다. 
# 결과 화별로 다음과 같은 내용을 저장합니다. 영화 대표코드, 영화명(국문), 영화명(문), 영화명(원문) ,관람등급, 개봉연도, 상시간, 장 르, 감독명 해당 결과를 movie.csv에 저장합니다. 
# (선택) 배우 정보, 배급사 정보 등을 추가적으로 수집할 수 있습니다. 

import requests, json
import csv
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint


result = []
with open('boxoffice.csv', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)


    for row in reader:
       code = row.get('movieCd')
       result.append(code)
# print(type(result))

results = {}
for code_new in result:
    
    key = config('S_KEY')
    
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={code_new}'
    api_data = requests.get(url).json()

    movies = api_data.get('movieInfoResult').get('movieInfo')
    # for movie in movies: # 굳이 이건 넣을 필요가 없음 어차피 자료 1에서 자료를 불러오는 값들이라서. 
    #     code_new = movie.get('movieCd')
    code_new = movies.get('movieCd')
#     if code in result:
    results[code_new] = {
        'movieCd' : movies.get('movieCd'),
        'movieNm' : movies.get('movieNm'),
        'movieNmEn' : movies.get('movieNmEn'),
        'movieNmOg' : movies.get('movieNmOg'),
        'watchGradeNm' : movies.get('audits')[0].get('watchGradeNm') if movies.get('audits') else None, # JSON 파일을 자세히 보면 인덱스 대가로로 들어간 것들이 있다.
        # 이부분을 안해서 첨엔 이상하게 나옴
        # 그래서 인덱스인 [0] 인 넣고 조건표현식을 넣음
        'openDt' : movies.get('openDt'),
        'showTm' : movies.get('showTm'),
        'genreNm' : movies.get('genre')[0].get('genreNm') if movies.get('genre') else None,
        'peopleNm' : movies.get('directors')[0].get('peopleNm')if movies.get('directors') else None
        }
pprint(results) 
with open('movies.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genreNm', 'peopleNm']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in results.values():
        writer.writerow(value)











        # print(row['movieCd'])
        # print(row['movieNm'])
        # print(row['movieNm En'])
        # print(row['movieNm Og'])
        # print(row['watchGradeNm'])
        # print(row['openDt'])
        # print(row['showTm'])
        # print(row['genreNm'])
        # print(row['peopleNm'])


# for movieCd in movie_list:


# dicts = {}
# for movieCd in movieCd_list:
#     url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={code_new}'
#     api_data = requests.get(url).json()

#     print(response[])