# https://api.odcloud.kr/api/15062521/v1/uddi:eae85cb4-2542-40d9-a2e2-aa7b2b9a8ebd?page=1&perPage=100&serviceKey=p1uy20oHBITh1a%2BSb55WOVvytQZTEG2r93hX0ZH%2BC9e6ATIA6tLbo8kU7vE0pv09J9diEpveymRrGGzlQpRzZg%3D%3D


from bs4 import BeautifulSoup
import urllib.request
import xml.dom.minidom
import requests
import json
from pandas.io.json import json_normalize
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

import collections
"""url_ex = 'http://data.ex.co.kr/openapi/basicinfo/unitList?key=1681441752&type=json&numOfRows=1000&pageNo=1'

req =requests.get(url_ex)
jsondata_ex = json.loads(req.text)
exdata1 = pd.json_normalize(jsondata_ex['unitLists'])
exdata1.columns
exdata1[:][['unitName','unitCode']]

exdata_pg = jsondata_ex['pageSize']

for i in range(2,exdata_pg+1):
    url_ex ='http://data.ex.co.kr/openapi/basicinfo/unitList?key=1681441752&type=json&numOfRows=1000&pageNo='+str(i)
    req =requests.get(url_ex)
    jsondata_ex = json.loads(req.text) 
    temp = pd.json_normalize(jsondata_ex['unitLists'])
    exdata1 = exdata1.append(temp, ignore_index=True)

exdata1 # 톨게이트 코드, 톨게이트명

"""

###http://data.ex.co.kr/openapi/basicinfo/openApiInfoM?apiId=0110 이건 실시간 정보만 제공해서 무쓸모네

# 고속도로 공공데이터 포털을 이용하자

# 요일/월별 변동계수 라는게 있네 실제자료도 좋지만 이거 계수를 경험식에 쓰면 좋을거같다
# http://data.ex.co.kr/portal/docu/docuList?datasetId=9&serviceType=ORG&keyWord=&searchDayFrom=2014.12.01&searchDayTo=2021.11.15&CATEGORY=&GROUP_TR=


# 주요구간 선정
# 주요구간 연도별 차종별 일평균 교통량(2016년_2020년).csv

exdata = pd.read_csv('C:\\Users\\gijeo\\Desktop\\TCS_영업소간교통량_1일_1일_20211101\\주요구간 연도별 차종별 일평균 교통량(2016년_2020년).csv', encoding='cp949')

exdata[exdata['구분(단위:대/년)'].str.contains('가산JC')]
exdata[0:30]
arrive = []
departure = []
for i in exdata['구분(단위:대/년)']:
    departure.append(i.strip().split('~')[0])
    arrive.append(i.strip().split('~')[1])


set(exdata['구분(단위:대/년)'])
departure
len(set(departure))
len(set(arrive))
arrive

"""
namepatch: 동명의 지명이 있는 경우 이름이 긴 것을 패치한다. 딕셔너리형으로 정의했음

key: 도 이름 초성 영어
value: IC/JC이름 초성 영어

e.g., namepatch['경기광주']='GG_GGGJ'
"""
namekeys = ['경기광주','금산사','남원주',   '서울산','서울주','연화산']
namepatch= {'경기광주':'GG_GGGJ', '금산사':'JB_GSS','남원주':'GW_NWJ',   '서울산':'US_SUS','서울주':'US_SUJ','연화산':'GN_YHS' }
np.setdiff1d(ar, dp)

dp = Series(sorted(list(set(departure))))
for i in namekeys:
    dp = dp.str.replace(i,namepatch[i])

ar = Series(sorted(list(set(arrive))))
for i in namekeys:
    ar = ar.str.replace(i,namepatch[i])


province_dp_matching= [] #np.full(len(set(departure)),'')
province_ar_matching= []

sorted(list(set(departure)))
sorted(list(set(arrive)))
province_dict = {'서울':['서울'], #1
#'인천':[], #0
'세종':['세종'], #1
'대전':['대전','계룡','노은','비룡','산내',     '신탄진','유성'], #7
'광주':['광주'], #1
'대구':['대구','금호','달성','도동','수성',     '옥포','유천','현풍' ], #8
'부산':['가락','금정','기장','냉정','노포',     '일광','철마','해운대'], #7
'울산':['문수','범서','언양','온양','울주',     '통도사', 'US_SUS', 'US_SUJ'], #7
'경기':['곤지암','군자','군포','금곡','기흥',   '광명','남양주', '대신', '덕평', '동탄',          '둔대', '마성', '마장', '매송', '발안',      '봉담', '부곡','비봉', '서종', '송산',           '송탄', '수원', '안산', '안성', '양감',     '양지', '양평', '여주', '오산', '이천',             '장안', '장지', '청북', '평택', 'GG_GGGJ'], #34
'강원':['강릉','강촌','근덕','내촌','대관령',   '둔내', '동산', '동해', '만종', '망상',           '면온', '문막', '새말', '속사', '신림',      '신평', '양양', '원주', '조양', '춘천',          '홍천', 'GW_NWJ'], #23
'충남':['고덕','공주','광천','금산','논산',    '당진', '대천', '마곡사', '목천', '무창포',      '서산', '서천', '송악', '신양', '연무',     '예산', '정안', '천안', '풍세', '해미'], #19
'충북':['감곡','괴산','구병산','금강','금왕',    '남이', '단양', '대소', '문의', '보은',       '삼성', '속리산', '영동', '오창', '옥산',     '제천', '중앙탑', '증평', '청주', '충주',          '회인'], #20
'경북':['가산','건천','경산','경주','고령',    '구미', '군위', '기계', '김천', '낙동',          '다부', '도개', '문경','북안', '상주',      '성주', '신녕', '안동', '영주', '영천',             '왜관', '의성', '포항', '청송', '청통',     '추풍령', '화산'], #26
'경남':['가조','거창','고성','곤양','광재',    '군북', '김해', '남지', '단성', '대감',          '대동', '대청', '마산', '문산','물금',      '밀양', '배내골', '사천', '산인', '산청',           '삼랑진', '생초', '서상', '양산', '연화산',     '영산', '지곡', '지수','진교', '진례',           '진영', '진주','진해', '창녕', '창원',         '칠서', '칠원', '통영', '함양', 'GN_YHS'], #38
'전북':['고창','군산','김제','남원','내장산',       '덕유산', '삼례', '상관', '전주', '선운산',    '소양', '오수', '완주', '익산', '장수',       '정읍','지리산', 'JB_GSS'], #18
'전남':['강진','고서','고흥','곡성','광양',    '구례', '나주', '담양', '대덕', '목포',          '무안', '백양사', '벌교', '보성', '석곡',     '순천', '승주', '영광', '옥곡', '장성',           '진월','함평'] #22
}


# 광명, 군자는 인천이랑 이어지는곳인데 인천에 ic가 없어서 걸러지지가 않는다..음.. 고민좀 해야함

# dp, ar
idx=0
for i in dp: 
    jkey=0
    jval=0
    kidx=0
    for jkey, jval in province_dict.items():
        jval_lst = list(jval)
        try:
            for kidx in jval_lst:
                if (Series(i).str.contains(kidx).astype('int32').sum()==1) :
                    province_dp_matching.append(jkey)
        except:
            province_dp_matching.append('check')
    print(idx, i, province_dp_matching[idx])
    idx+=1

idx=0
ar[93]
for i in ar: 
    jkey=0
    jval=0
    kidx=0
    for jkey, jval in province_dict.items():
        jval_lst = list(jval)
        try:
            for kidx in jval_lst:
                if (Series(i).str.contains(kidx).astype('int32').sum()==1) :
                    province_ar_matching.append(jkey)
        except:
            province_ar_matching.append('check')
    print(idx, i, province_ar_matching[idx])
    idx+=1

len(province_dp_matching)
len(dp)
len(province_ar_matching)
len(ar)
dp


dp[0]
province_dict.values()
list(set(departure))

