# 1-파이썬을 활용한 데이터 수집1

프로젝트 요약 : 

영화진흥위원회 오픈 API 를 이용하여 최근 50주간 데이터 중에 주간 박스오피스 데이터를 수집하였습니다. 수집한 데이터를 가지고 활용하여 csv 파일로 저장하였습니다. 

이 프로젝트를 통해 조건/반복문 및 다양한 자료구조 활용과 api 주소를 가지고 필요한 데이터 형태를 가공하는 법을 알 수 있었습니다. 

- 01.py

  - 맨 처음 import json을 넣은 이유는 json type을 dictionary type으로 변경하기 위해 넣었습니다.

  - ```python
    for week in range(50):
    ```

    - 예를 들면 for i in range(3)이라 놓고 print(i) 를 하면 0/1/2 값이 출력됩니다. 그래서 처음에는 총 50주라고 하여 51주를 넣었습니다. 하지만  datetime이라는 (2019, 7, 13) 값을 넣어 빼기를 하였으므로 50주로 변경하였습니다.

  - 50주부터 날짜 빼기를 하려면 timedelta를 넣어야한다고 교수님께서 알려주셨습니다.

    - timedelta(weeks=1) 일주일 이전의 시간을 구함

      timedelta(weeks=i) 이면 -i 이전의 시각을 구함 

  - ```python
    if code not in result:
    ```

    - if code in result 라고 처음에 작성하였습니다. 하지만 여기서는 not을 붙여야 했습니다. 왜냐하면 날짜를 거꾸로 돌아가면서 데이터를 얻기때문에 최신 값이 남아있고 그 다음에 중복되는 영화 값은 다 제외시키는 역할을 알게 되었습니다.

- 02.py

  - ```python
    for movie in movies:
        code_new = movie.get('movieCd')
    ```

    - 처음엔 for 문을 넣었지만 생각해보니 01.py에서 자료를 불러오는 값들이라서 필요가 없음을 깨닫고 지웠습니다. 

  - ```python
    'movieCd' : movies.get('movieCd'),
    'movieNm' : movies.get('movieNm'),
    'movieNmEn' : movies.get('movieNmEn'),
    'movieNmOg' : movies.get('movieNmOg'),
    ```

    - 처음엔 이런식으로 쭉 작성을 하였고 터미널에서 값을 출력해보니 이상하게 나타났다. 교수님께서는 json을 열어 제대로 보면 딕셔너리가 또 다시 들어간 부분이 있으니 이 부분을 잘 생각해서 코드를 작성하라고 하셨습니다. 

    - ```python
      "genres": [
              {
                "genreNm": "사극"
              },
              {
                "genreNm": "드라마"
              }
            ],
      ```

    - 이런 식으로 리스트 안에 딕셔너리로 작성된 key 값들(watchGradeNm, genreNm, peopleNm) 있었습니다.

    - ```python
      'genreNm' : movies.get('genre')[0].get('genreNm') if movies.get('genre') else None
      ```

    - 즉, get(x) 함수라고 한다면 x라는 key에 대응되는 value를 돌려준다는 뜻으로 genres 라는 리스트 안에 genreNm 이라는 키 값이 필요한 것이므로 인덱스이고 첫번째 시작을 표시하는 [0]을 넣고 조건 표현식을 달았습니다.
  
- 03.py

  - ```python
    movies = api_data.get('peopleListResult').get('peopleList')
    pprint(movies)
    ```

    - 이 부분에서 프린트를 하였더니 감독 / 배우 등등 분류가 있다는 것을 알게 되었습니다. 그래서 if 절이 들어가야 한다는 것을 깨닫게 되었습니다. 

  - ```python
    movies = api_data.get('peopleListResult').get('peopleList')
    code_new = movies.get('peopleCd')
    rep_rol = movies.get('repRoleNm')
    ```

    - 처음에 이렇게 하였더니 atrributeError인 list object has no attribute 'get'이라는 오류가 발생되었습니다.
    - 오류가 난 이유를 모르겟어서 json 파일을 열어 다시 꼼꼼히 읽어보았습니다.

  - ```json
    {
      "peopleListResult": {
        "totCnt": 178332,
        "peopleList": [
          {
            "peopleCd": "20328592",
            "peopleNm": "다미앙 마니벨",
            "peopleNmEn": "Damien MANIVEL",
            "repRoleNm": "감독",
            "filmoNames": "이사도라의 아이들"
          },
    ```

    - 여기서 제가 놓친 부분으 "peopleList" 다음 [] <-이 모양으로 표시되어 있었습니다. 이 부분을 작성하지 않아서 get 오류가 난 것으로 생각이 되었습니다. 

  - ```python
    movies = api_data.get('peopleListResult').get('peopleList')[0]
    ```

    - 02.py에서 했던 것 처럼 [0] 이라는 인덱스 첫번째 값을 뒤에 작성하였더니 작동되었다. 
    - 이후 프린트를 하였을 때 이상하게 한개만 프린트가 되었습니다. 
      - {'20328592': {'filmoNames': '이사도라의 아이들',
                      'peopleCd': '20328592',
                      'peopleNm': '다미앙 마니벨',
                      'repRoleNm': '감독'}}

  - 맨 처음 코드 작성한 부분을 다시 한번 읽어보았습니다. 

  - ```python
    #맨 처음 작성한 코드 (일정부분은 생략)
    results = {}
    for code_new in result:
        key = config('S_KEY')
        
        url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleCd={code_new}'
        api_data = requests.get(url).json() 
    
        
    
        movies = api_data.get('peopleListResult').get('peopleList')[0]
       
        for people in movies:
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
    ```

    - for people in movies:  라는 for 문을 굳이 넣을 필요가 없었습니다. 왜냐하면 이미 02.py 에서 불러왔기 때문에 for문을 제외 시켰습니다. 
    - 또한 people 이라는 변수와 code_new 라는 변수가 이상하게 써져있어서 다시 code_new라는 값으로 바꿔서 썼습니다. 
    - 다음으로 if not in and 구문을 넣어 중복을 제외 시켰습니다. 



