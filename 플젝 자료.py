# -*- coding: utf-8 -*-
"""
1-1. 총인구 접종률 파일 (누적)
1-2. 일별 접종자수 파일 

2-1. 월별 외국인 입국자수
2-2 (대륙별) 외국인 입국자수

3. 제주도 월별 입도자수

"""

1-1. 총인구 접종률 파일 (누적)
[컬럼목록]
'일자',
'1차접종률_총인구',
'2차접종률_총인구'
'부스터샷접종률_총인구'

[날짜] 
- 2021. 2. 26 ~ 2021. 11. 11


[데이터 불러오기]
import pickle
# 데이터 불러오기
file = open('c:/p1/vac_clear.pkl', 'rb') 
vac_per = pickle.load(file)
file.close() 
vac_per


1-2. 일별 접종자수 파일 
[컬럼목록]
'일자',
'1차_일별',
'2차_일별',
'일별_부스터샷'

[날짜] 
- 2021. 2. 26 ~ 2021. 11. 11


[데이터 불러오기]
import pickle
# 데이터 불러오기
file = open('c:/p1/vac_daily.pkl', 'rb') 
vac_daily = pickle.load(file)
file.close() 
vac_daily


[특이사항]
2월 26일 데이터에는 국외에서 접종한 건이 포함되어있습니다. (주한미군, 대사관 관계자등)

#----------------------------------------------------------------------------------------------

2-1. 월별 외국인 입국자수
[컬럼목록]
'등록날짜' # 입국월 정보
'최종합계(승무원 제외)',


[날짜] 
- 2019. 8. ~ 2021. 9


[데이터 불러오기]
import pickle
# 데이터 불러오기
file = open('c:/p1/f_all_clear.pkl', 'rb') 
foreign = pickle.load(file)
file.close()

[특이사항]
법무부 월별 자료 10월 데이터는 11월 중순 이후 업데이트 가능


2-2 (대륙별) 외국인 입국자수
[컬럼목록] 
 0   등록날짜    26 non-null     datetime64[ns]
 1   기타      26 non-null     int32         
 2   남아메리카주  26 non-null     int32         
 3   북아메리카주  26 non-null     int32         
 4   아시아주    26 non-null     int32         
 5   아프리카주   26 non-null     int32         
 6   오세아니아주  26 non-null     int32         
 7   유럽주     26 non-null     int32         
 8   총합계     26 non-null     int32  

[데이터 불러오기]
import pickle
# 데이터 불러오기
file = open('c:/p1/f_all_con.pkl', 'rb') 
foreign = pickle.load(file)
file.close()

#----------------------------------------------------------------------------------------------

3. 제주도 월별 입도자수
[컬럼목록]
'입도일'
'입도자수'


[날짜] 
- 2019. 8. ~ 2021. 9


[데이터 불러오기]
import pickle
# 데이터 불러오기
file = open('c:/p1/jeju.pkl', 'rb') 
jeju = pickle.load(file)
file.close() 






