import pandas as pd
from pandas import DataFrame, Series
geton = pd.read_csv('srt_monthly_geton_2019-2021.csv',encoding='cp949')
getoff = pd.read_csv('srt_monthly_getoff_2019-2021.csv',encoding='cp949')

geton.info()
getoff.info()
province_lst = ['서울','경기','경기','대전','충남','충남','충북','대구','경북','경북','울산','부산','광주','전남','전남','전북','전북']
city_lst = ['수서','동탄', '지제','대전', '공주', '천안아산', '오송', '동대구', '김천구미', '신경주','울산','부산','광주송정','나주','목포','익산','정읍']
srt_province = DataFrame( city_lst, index=province_lst)
srt_province.info()
srt_province.reset_index(inplace=True)

srt_province.info()
srt_province.columns = ['도명','역명']

geton = geton.T   # 행: 시간 순
getoff = getoff.T 

geton.columns = geton.iloc[0]
getoff.columns = getoff.iloc[0]

geton = geton.iloc[1:,]
getoff = getoff.iloc[1:,]

geton=  geton.T  #행: 역명
getoff = getoff.T
geton_merge = pd.merge(srt_province, geton, how='inner', left_on='역명', right_on = '승차역')
getoff_merge = pd.merge(srt_province, getoff, how='inner', left_on='역명', right_on = '하차역')
getoff_merge
geton_merge.역명 = geton_merge.역명 + '출발'
getoff_merge.역명 = getoff_merge.역명 + '도착'
geton_merge.도명 = geton_merge.도명 + '출발'
getoff_merge.도명 = getoff_merge.도명 + '도착'

getoff_merge
geton_merge

passengers = pd.concat([geton_merge, getoff_merge],axis=0)
temp = passengers.groupby('도명').sum()

temp.reset_index(inplace=True)
temp[['도명','역명']]
temp.columns
temp2 = temp[['도명','2019년 1월', '2019년 2월', '2019년 3월', '2019년 4월', '2019년 5월', '2019년 6월',
       '2019년 7월', '2019년 8월', '2019년 9월', '2019년 10월', '2019년 11월', '2019년 12월', 
       '2020년 1월', '2020년 2월', '2020년 3월', '2020년 4월', '2020년 5월', '2020년 6월', 
       '2020년 7월', '2020년 8월', '2020년 9월','2020년 10월', '2020년 11월', '2020년 12월',
       '2021년 1월', '2021년 2월', '2021년 3월', '2021년 4월', '2021년 5월', '2021년 6월',
       '2021년 7월', '2021년 8월','2021년 9월']]
temp2.info()
temp2 = temp2.rename(columns={'도명':'일시'})
temp2.행선지방향
temp2 = temp2.T
temp2.reset_index(inplace=True)
temp2.columns = temp2.iloc[0]
temp2 = temp2[1:]
temp2.columns
temp2.index
temp2


#pd.to_datetime(i,format='%Y-%m-%d')

import time
year = temp2['일시'][:].str[0:4]
month = temp2['일시'][:].str[-3:-1].str.lstrip().str.zfill(2)
date = Series(year+'-'+month)
temp2.일시 = pd.to_datetime(date, format='%Y-%m')
temp2
temp2.to_pickle('srt_monthly_passengers.pkl')