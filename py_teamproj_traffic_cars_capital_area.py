import pandas as pd
from pandas import DataFrame, Series
from pandas.io.parquet import read_parquet
from pandas.io.pickle import read_pickle

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


# 일일/월간 수도권 출입차량수(타지역<->수도권)
#일일
syr='2021'

traffic_capital_area = pd.read_pickle('c:/Python_workdir/finalproj/traffic/traffic_capital_area_daily_'+syr+'.pkl')

datelist_str = Series(pd.to_datetime(traffic_capital_area['집계일자'].unique(),format='%Y-%m-%d')).astype('str').tolist() #daily
datelist_str
traffic_capital_area.집계일자 = Series(pd.to_datetime(traffic_capital_area['집계일자'],format='%Y-%m-%d')).astype('str')
res= DataFrame()
for i in datelist_str:
    #i = datelist_str[0]
    wheredata  = (traffic_capital_area['집계일자']==i)
    wheredata2 = ~ ((traffic_capital_area['출발도명']=='수도권')&(traffic_capital_area['도착도명']=='수도권'))
    #traffic_capital_area[wheredata2]

    oneday_departure = traffic_capital_area[wheredata&wheredata2].groupby('출발도명').sum().loc['수도권',['도착지방향1종교통량', '도착지방향2종교통량', '도착지방향3종교통량', '출발지방향1종교통량', '출발지방향2종교통량', '출발지방향3종교통량']]
    temp = pd.concat([ oneday_departure,Series(i)], axis=0)
    res = res.append(temp, ignore_index=True)

res
res.columns
res.rename(columns={0:'집계일자',    '도착지방향1종교통량':'수도권출발1종교통량', '도착지방향2종교통량': '수도권출발2종교통량' , '도착지방향3종교통량':'수도권출발3종교통량' , '출발지방향1종교통량':'수도권도착1종교통량', '출발지방향2종교통량': '수도권도착2종교통량', '출발지방향3종교통량': '수도권도착3종교통량'}, inplace=True)

res.to_pickle('ex_traffic_in_n_out_capitalarea_daily_'+syr+'.pkl')

data2019 = pd.read_pickle('ex_traffic_in_n_out_capitalarea_daily_2019.pkl')

data2020 = pd.read_pickle('ex_traffic_in_n_out_capitalarea_daily_2020.pkl')

data2021 = pd.read_pickle('ex_traffic_in_n_out_capitalarea_daily_2021.pkl')

datamerge = pd.concat([data2019, data2020,data2021],axis=0)
datamerge.reset_index(inplace=True)
datamerge = datamerge[['집계일자', '수도권출발1종교통량', '수도권출발2종교통량', '수도권출발3종교통량', '수도권도착1종교통량', '수도권도착2종교통량', '수도권도착3종교통량']]

datamerge.to_pickle('ex_traffic_in_n_out_capitalarea_daily_2019-2021.pkl')
"""

    oneday_departure.rename(columns=['도착지방향1종교통량':'수도권출발1종교통량', '도착지방향2종교통량': '수도권출발2종교통량' , '도착지방향3종교통량':'수도권출발3종교통량' , '출발지방향1종교통량':'수도권도착1종교통량', '출발지방향2종교통량': '수도권도착2종교통량', '출발지방향3종교통량': '수도권도착3종교통량'])
"""

#월간
syr='2021'

traffic_capital_area = pd.read_pickle('c:/Python_workdir/finalproj/traffic/traffic_capital_area_daily_'+syr+'.pkl')

datelist_str = Series(pd.to_datetime(traffic_capital_area['집계일자'].unique(),format='%Y-%m')).astype('str').str[:-3].unique().tolist() #monthly

traffic_capital_area = pd.read_pickle('c:/Python_workdir/finalproj/traffic/traffic_capital_area_daily_'+syr+'.pkl')

datelist_str = Series(pd.to_datetime(traffic_capital_area['집계일자'].unique(),format='%Y-%m')).astype('str').str[:-3].unique().tolist() #monthly

datelist_str
traffic_capital_area.집계일자 = Series(pd.to_datetime(traffic_capital_area['집계일자'],format='%Y-%m-%d')).astype('str').str[:-3]
res= DataFrame()

for i in datelist_str:
    #i = datelist_str[0]
    wheredata  = (traffic_capital_area['집계일자']==i)
    wheredata2 = ~ ((traffic_capital_area['출발도명']=='수도권')&(traffic_capital_area['도착도명']=='수도권'))
    #traffic_capital_area[wheredata2]

    oneday_departure = traffic_capital_area[wheredata&wheredata2].groupby('출발도명').sum().loc['수도권',['도착지방향1종교통량', '도착지방향2종교통량', '도착지방향3종교통량', '출발지방향1종교통량', '출발지방향2종교통량', '출발지방향3종교통량']]
    temp = pd.concat([ oneday_departure,Series(i)], axis=0)
    res = res.append(temp, ignore_index=True)

res
res.columns
res.rename(columns={0:'집계일자',    '도착지방향1종교통량':'수도권출발1종교통량', '도착지방향2종교통량': '수도권출발2종교통량' , '도착지방향3종교통량':'수도권출발3종교통량' , '출발지방향1종교통량':'수도권도착1종교통량', '출발지방향2종교통량': '수도권도착2종교통량', '출발지방향3종교통량': '수도권도착3종교통량'}, inplace=True)

res.to_pickle('ex_traffic_in_n_out_capitalarea_monthly_'+syr+'.pkl')

data2019 = pd.read_pickle('ex_traffic_in_n_out_capitalarea_monthly_2019.pkl')

data2020 = pd.read_pickle('ex_traffic_in_n_out_capitalarea_monthly_2020.pkl')

data2021 = pd.read_pickle('ex_traffic_in_n_out_capitalarea_monthly_2021.pkl')

datamerge = pd.concat([data2019, data2020,data2021],axis=0)
datamerge.reset_index(inplace=True)
datamerge = datamerge[['집계일자', '수도권출발1종교통량', '수도권출발2종교통량', '수도권출발3종교통량', '수도권도착1종교통량', '수도권도착2종교통량', '수도권도착3종교통량']]

datamerge.to_pickle('ex_traffic_in_n_out_capitalarea_monthly_2019-2021.pkl')