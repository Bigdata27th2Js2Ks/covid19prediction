from bs4 import BeautifulSoup
import urllib.request
import xml.dom.minidom
import requests
import json
from pandas.io.json import json_normalize
from pandas import DataFrame
import pandas as pd

#SRT정보는 api encoding key, decoding key를 홈페이지에 입력하면 자동으로 url을 생성해준다 잘되넹
url_srt_weekly = "https://api.odcloud.kr/api/15061851/v1/uddi:6e4f3e3a-3e75-4bc8-9dca-d9468da57fc5?page=1&perPage=100&serviceKey=p1uy20oHBITh1a%2BSb55WOVvytQZTEG2r93hX0ZH%2BC9e6ATIA6tLbo8kU7vE0pv09J9diEpveymRrGGzlQpRzZg%3D%3D"


req = requests.get(url_srt_weekly)
jsondata_srt_weekly = json.loads(req.text)
srt_weekly = pd.json_normalize(jsondata_srt_weekly['data'])
srt_weekly_2020_1sthalf = srt_weekly
srt_weekly_2020_1sthalf.to_csv('srt_weekly_2020_1sthalf.csv')

srt_weekly = pd.read_csv('srt_weekly_2020_1sthalf.csv')
srt_weekly.head()
srt_weekly.set_index('Unnamed: 0', inplace=True)
srt_weekly.columns
"""['공주', '광주송정', '구분', '김천구미', '나주', '대전', '동대구', '동탄', '목포', '부산', '수서',
       '승하차', '신경주', '오송', '울산', '익산', '정읍', '지제', '천안아산']"""

srt_weekly=srt_weekly[['구분','승하차', '공주', '광주송정', '김천구미', '나주', '대전', '동대구', '동탄', '목포', '부산', '수서', '신경주', '오송', '울산', '익산', '정읍', '지제', '천안아산']]

"""
SRT 도별 역
서울 - '수서'
경기 - '동탄', '지제'
대전 - '대전'
충남 - '공주', '천안아산'
충북 - '오송'
대구 - '동대구'
경북 - '김천구미', '신경주'
울산 - '울산'
부산 - '부산'
광주 - '광주송정'
전남 - '나주', '목포' 
전북 - '익산', '정읍'
"""
srt_weekly.to_csv('srt_weekly_2020_1sthalf.csv')
#srt_weekly_province 

province_lst = ['서울','경기','경기','대전','충남','충남','충북','대구','경북','경북','울산','부산','광주','전남','전남','전북','전북']
city_lst = ['수서','동탄', '지제','대전', '공주', '천안아산', '오송', '동대구', '김천구미', '신경주','울산','부산','광주송정','나주','목포','익산','정읍']
srt_province = DataFrame( city_lst, index=province_lst)
srt_province.columns=['역명']
srt_province.reset_index(inplace=True)
srt_province.columns=['지역','역명']
srt_province

srt_weekly.columns
srt_weekly_geton = srt_weekly[srt_weekly.승하차=='승차'][['구분','공주', '광주송정', '김천구미', '나주', '대전', '동대구', '동탄', '목포', '부산', '수서', '신경주', '오송', '울산', '익산', '정읍', '지제', '천안아산']]
srt_weekly_getoff = srt_weekly[srt_weekly.승하차=='하차'][['구분','공주', '광주송정', '김천구미', '나주', '대전', '동대구', '동탄', '목포', '부산', '수서', '신경주', '오송', '울산', '익산', '정읍', '지제', '천안아산']]
srt_weekly_geton = srt_weekly_geton.T
srt_weekly_getoff = srt_weekly_getoff.T
srt_weekly_geton.columns = srt_weekly_geton.iloc[0,:]
srt_weekly_getoff.columns = srt_weekly_getoff.iloc[0,:]

srt_weekly_geton = srt_weekly_geton[1:]
srt_weekly_getoff = srt_weekly_getoff[1:]

temp = pd.merge(srt_province, srt_weekly_geton, left_on='역명',right_index=True)
temp.columns
temp  = temp.groupby(temp.index).sum()

temp2 = pd.merge(srt_province, srt_weekly_getoff, left_on='역명',right_index=True)
temp2
temp2 = temp2.groupby(temp2.index).sum()

srt_weekly_geton_province = temp
srt_weekly_getoff_province = temp2
srt_weekly_geton_province.to_pickle('srt_weekly_geton_province.pkl')
srt_weekly_getoff_province.to_pickle('srt_weekly_getoff_province.pkl')
