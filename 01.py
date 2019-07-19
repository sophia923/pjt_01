import requests, json
import csv
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint

url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?'
current_date = datetime(2019, 7, 13)


result = {}

for week in range(50): #range가 하나 빼는 거라서 51로 넣었는데 알고비 50 근데 왜 50을 넣어야함 ? 인덱스가 0부터 시작하니까 그ㅐㄹ서 뭐 ? 레인지에 5를 넣고 0-4까지 나
    # 자기 자신을 뺐으니까 50이이여도 상관없다 date time 을 뺐으니까 50을 해도 상관이 없다 이건 시행착오 
    key = config('S_KEY')
    cal_date = current_date - timedelta(weeks=week) 
    targetDt = cal_date.strftime('%Y%m%d')
    # print(week)

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?weekGb=0&key={key}&targetDt={targetDt}'
    api_data = requests.get(url).json()
    # pprint(api_data)

    # res = requests.get(url)
    # text = res.text

    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    for movie in movies:
            code = movie.get('movieCd')
        # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
        # 그게 가장 마지막 주 데이터다. 즉 기존 영화 코드가 있다면 딕셔너리에 넣지 않는다. 
            if code not in result: # not을 안붙임 근데 여기선 not을 붙였었다. 중복을 피하기 위해 / ㄹㅔ인지가 7월 13일부터 돌아가는데 
                # 최신것이 가장 남아있고 그 다음 전날에 들어오는 중복되는 영화들은 값은 다 제외시키는 것임 시행착오
                result[code] = {
                    'movieCd' : movie.get('movieCd'),
                    'movieNm' : movie.get('movieNm'),
                    'audiAcc' : movie.get('audiAcc')
                }
    # pprint(result)

with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)







































#     for j in range(3):
#         movies_dict['코드명'] = movies[j].get('movieCd')
#         movies_dict['영화명'] = movies[j].get('movieNm')
#         movies_dict['누적관객수'] = movies[j].get('audiAcc')
#         movies_list.append(movies_dict)
# print(movies_list)      

    # for i in movies:

    #     print(i['movieCd'],i['movieNm'], i['audiAcc'])


# with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
#     reader = csv.DictReader(f)
# # movieCd(실제 movieCd코드)가 딕셔너리의 key가 되고 
		# movieCd / movieNm / audiAcc) -> 필드: movieCd / mmovieNm / audiAcc -> 값



# res = requests.get(url)
# text = res.text
# # print(text)

# easyview = json.loads(text)
# # print(easyview)


# for i in easyview['boxOfficeResult']['weeklyBoxOfficeList']:
#     print(i['movieCd'],i['movieNm'], i['audiAcc'])

# # #movieCd = 영화대표코드
#movieNm = 영화명
#audiCnt = 해당일의 관객수를 출력합니다.
#audiAcc = 	누적관객수를 출력합니다.


# pprint 사용하기

# from datetime import datetime, timedelta
# datetime(2019, 7, 13) - (ㅃㅐ야함)
# timedelta(weeks=1) 일주일 이전의 시간을 구함
#timedelta(weeks=i) 이면 -i 이전의 시각을 구함 
#strftime('%Y%m%d') ==>20190713 처럼 ㄷ나옴 (import안해도됨)
#targetDt.strftime('%Y%m%d')