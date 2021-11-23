import pandas as pd
from pandas import DataFrame, Series

syr= '2021'
traffic = pd.read_pickle('C:\\Python_workdir\\finalproj\\traffic\\ex_traffic_daily_province_merge_v2_'+syr+'.pkl')

traffic.info()
traffic_capital_area = traffic[ ((traffic['출발도명']=='서울')|(traffic['출발도명']=='경기')|(traffic['출발도명']=='인천')) | ((traffic['도착도명']=='서울')|(traffic['도착도명']=='경기')|(traffic['도착도명']=='인천')) ]

traffic_capital_area.loc[((traffic['출발도명']=='서울')|(traffic['출발도명']=='경기')|(traffic['출발도명']=='인천')),['출발도명']] = '수도권'

traffic_capital_area.loc[((traffic['도착도명']=='서울')|(traffic['도착도명']=='경기')|(traffic['도착도명']=='인천')),['도착도명']] = '수도권'


datelist_str = Series(pd.to_datetime(traffic_capital_area['집계일자'].unique(),format='%Y-%m-%d')).astype('str').tolist()

traffic_capital_area['집계일자'] =Series(pd.to_datetime(traffic_capital_area['집계일자'],format='%Y-%m-%d')).astype('str')

df_traffic_capita_area = DataFrame(columns=['집계일자', '출발도명', '도착도명', '도착지방향1종교통량', '도착지방향2종교통량', 
'도착지방향3종교통량', '출발지방향1종교통량', '출발지방향2종교통량', '출발지방향3종교통량'])

for i in datelist_str:
#    i = datelist_str[0]
    temp = traffic_capital_area[traffic_capital_area['집계일자']==i].groupby(['출발도명','도착도명']).sum()
    temp.reset_index(inplace=True)
    tempdate = Series([i for j in range(len(temp))])
    temp = pd.concat([tempdate, temp], axis=1)
    temp = temp.rename(columns={0:'집계일자'})

    df_traffic_capita_area = df_traffic_capita_area.append(temp, ignore_index=True)

df_traffic_capita_area.집계일자 = pd.to_datetime(df_traffic_capita_area.집계일자, format= '%Y-%m-%d')
df_traffic_capita_area.to_pickle('c:/Python_workdir/finalproj/traffic/traffic_capital_area_daily_'+syr+'.pkl')



# monthly merge
datelist_str = Series(pd.to_datetime(traffic_capital_area['집계일자'].unique(),format='%Y-%m')).astype('str').str[:-3].unique().tolist()
temp1 = DataFrame(traffic_capital_area.loc[:,'집계일자'].str[:-3])
temp1.columns = ['집계연월']

traffic_capital_area

temp = pd.concat([temp1, traffic_capital_area], axis=1)

df_traffic_capital_area = DataFrame(columns=['집계연월', '출발도명', '도착도명', '도착지방향1종교통량', '도착지방향2종교통량', 
'도착지방향3종교통량', '출발지방향1종교통량', '출발지방향2종교통량', '출발지방향3종교통량'])


for i in datelist_str:
    #i = datelist_str[3]
    temp2 = temp[temp['집계연월']==i].groupby(['출발도명','도착도명']).sum()
    temp2.reset_index(inplace=True)
    tempdate = DataFrame([i for j in range(len(temp2))], columns=['집계연월'])
    temp3 = pd.concat([tempdate, temp2], axis=1)

    df_traffic_capital_area = df_traffic_capital_area.append(temp3, ignore_index=True)

df_traffic_capital_area['집계연월'] = pd.to_datetime(
df_traffic_capital_area['집계연월'], format='%Y-%m')
df_traffic_capital_area.to_pickle('c:/Python_workdir/finalproj/traffic/traffic_capital_area_monthly_'+syr+'.pkl')