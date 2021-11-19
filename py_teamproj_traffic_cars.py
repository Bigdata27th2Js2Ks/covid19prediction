
import pandas as pd
from pandas import DataFrame, Series
from tensorflow.python.keras.backend import repeat_elements

namekeys = ['경기광주','금산사','남원주',   '서울산','서울주','연화산']
namepatch= {'경기광주':'GG_GGGJ', '금산사':'JB_GSS','남원주':'GW_NWJ',   '서울산':'US_SUS','서울주':'US_SUJ','연화산':'GN_YHS' }
province_dict = {'서울':['서울'], #1
#'인천':[], #0
'세종':['세종'], #1
'대전':['대전','계룡','노은','비룡','산내',     '신탄진','유성'], #7
'광주':['광주'], #1
'대구':['대구','금호','달성','도동','수성',     '옥포','유천','현풍' ], #8
'부산':['가락','금정','기장','냉정','노포',     '일광','철마','해운대'], #8
'울산':['문수','범서','언양','온양','울주',     '통도사', 'US_SUS', 'US_SUJ'], #8
'경기':['곤지암','군자','군포','금곡','기흥',   '광명','남양주', '대신', '덕평', '동탄',          '둔대', '마성', '마장', '매송', '발안',      '봉담', '부곡','비봉', '서종', '송산',           '송탄', '수원', '안산', '안성', '양감',     '양지', '양평', '여주', '오산', '이천',             '장안', '장지', '청북', '평택', 'GG_GGGJ'], #35
'강원':['강릉','강촌','근덕','내촌','대관령',   '둔내', '동산', '동해', '만종', '망상',           '면온', '문막', '새말', '속사', '신림',      '신평', '양양', '원주', '조양', '춘천',          '홍천', 'GW_NWJ'], #22
'충남':['고덕','공주','광천','금산','논산',    '당진', '대천', '마곡사', '목천', '무창포',      '서산', '서천', '송악', '신양', '연무',     '예산', '정안', '천안', '풍세', '해미'], #20
'충북':['감곡','괴산','구병산','금강','금왕',    '남이', '단양', '대소', '문의', '보은',       '삼성', '속리산', '영동', '오창', '옥산',     '제천', '중앙탑', '증평', '청주', '충주',          '회인'], #21
'경북':['가산','건천','경산','경주','고령',    '구미', '군위', '기계', '김천', '낙동',          '다부', '도개', '문경','북안', '상주',      '성주', '신녕', '안동', '영주', '영천',             '왜관', '의성', '포항', '청송', '청통',     '추풍령', '화산'], #27
'경남':['가조','거창','고성','곤양','광재',    '군북', '김해', '남지', '단성', '대감',          '대동', '대청', '마산', '문산','물금',      '밀양', '배내골', '사천', '산인', '산청',           '삼랑진', '생초', '서상', '양산', '연화산',     '영산', '지곡', '지수','진교', '진례',           '진영', '진주','진해', '창녕', '창원',         '칠서', '칠원', '통영', '함양', 'GN_YHS'], #40
'전북':['고창','군산','김제','남원','내장산',       '덕유산', '삼례', '상관', '전주', '선운산',    '소양', '오수', '완주', '익산', '장수',       '정읍','지리산', 'JB_GSS'], #18
'전남':['강진','고서','고흥','곡성','광양',    '구례', '나주', '담양', '대덕', '목포',          '무안', '백양사', '벌교', '보성', '석곡',     '순천', '승주', '영광', '옥곡', '장성',           '진월','함평'] #22
}

province_keys = []
province_vals = []

for i, j in province_dict.items():
    temp_vals = list(j)
    for k in temp_vals:
        province_vals.append(i)
        province_keys.append(k)

df_province = DataFrame(province_keys,province_vals)
df_province.reset_index(inplace=True)
df_province.columns=['도명','지명']
df_province

# csv to pkl
trafficdir = 'C:\\Python_workdir\\finalproj\\ex_traffic\\tcs_traffic\\'
traffic_flist = ['TCS_35_04_02_450209.txt','TCS_35_04_02_147770.txt','TCS_35_04_02_235755.txt',
                'TCS_35_04_02_842616.csv','TCS_35_04_02_116946.csv','TCS_35_04_02_171239.csv',
                'TCS_35_04_02_801019.txt','TCS_35_04_02_400036.txt','TCS_35_04_02_572313.txt',
                'TCS_35_04_02_528275.txt','TCS_35_04_02_281105.txt','TCS_35_04_02_918851.csv',

                'TCS_35_04_02_788323.csv','TCS_35_04_02_527939.csv','TCS_35_04_02_221961.csv',
                'TCS_35_04_02_575945.csv','TCS_35_04_02_822779.csv','TCS_35_04_02_921475.csv',
                'TCS_35_04_02_544083.csv','TCS_35_04_02_275276.csv','TCS_35_04_02_212164.csv',
                'TCS_35_04_02_497329.csv','TCS_35_04_02_667867.csv','TCS_35_04_02_443372.csv',

                'TCS_35_04_02_219275.csv','TCS_35_04_02_319193.csv','TCS_35_04_02_567217.csv',
                'TCS_35_04_02_770775.csv','TCS_35_04_02_643543.csv','TCS_35_04_02_388683.csv',
                'TCS_35_04_02_553483.csv','TCS_35_04_02_398541.csv','TCS_35_04_02_143681.csv',
                'TCS_35_04_02_502578.csv'
]

traffic_cols = ['집계일자','출발영업소코드','도착영업소코드','출발영업소명','도착영업소명','도착지방향1종교통량','도착지방향2종교통량','도착지방향3종교통량','출발지방향1종교통량','출발지방향2종교통량','출발지방향3종교통량']
idx = 10

for i in traffic_flist:
    df_traffic = DataFrame(columns=traffic_cols)
    if (i[-3:]=='txt'):
        temp  = pd.read_csv(trafficdir + i,sep='|',encoding='cp949',index_col = False,names=['집계일자','출발영업소코드','도착영업소코드','출발영업소명','도착영업소명','도착지방향1종교통량','도착지방향2종교통량','도착지방향3종교통량','도착지방향4종교통량','도착지방향5종교통량','도착지방향6종교통량','도착지방향총교통량','출발지방향1종교통량','출발지방향2종교통량','출발지방향3종교통량','출발지방향4종교통량','출발지방향5종교통량','출발지방향6종교통량','출발지방향총교통량'])
        print(idx, i)        
    else:
        temp = pd.read_csv(trafficdir + i,index_col = False, encoding='cp949')
        print(idx, i)
    #exdata1.append(temp, ignore_index=True)
    temp.출발영업소코드.astype('int32')
    temp.도착영업소코드.astype('int32')
    #df_traffic = df_traffic.append(temp.loc[(temp.출발영업소코드 < 991) & (temp.도착영업소코드 < 991) & (temp.출발영업소코드 != temp.도착영업소코드),traffic_cols], ignore_index=True)
    df_traffic = temp.loc[(temp.출발영업소코드 < 991) & (temp.도착영업소코드 < 991) & (temp.출발영업소코드 != temp.도착영업소코드),traffic_cols]
    pklname = 'ex_traffic_'+str(int(idx/12)+2019)+'_'+str((int(idx%12)+1)).zfill(2)+'.pkl'
    df_traffic.to_pickle(pklname)
    idx +=1

idx= 0

tt = temp2.groupby(['출발영업소명','도착영업소명']).count()
tt
idx=0
ifiles=0
suffix_name = str(int(ifiles/12)+2019)+'_'+str(int(ifiles%12)+1).zfill(2)+'.pkl'
temp2 = pd.read_pickle('ex_traffic_'+suffix_name)
print('ex_traffic_'+suffix_name+' start..!')

dp_toll = []
dp_city = []
dp_prov = []
ar_toll = []
ar_city = []
ar_prov = []
idx=0
tt.columns
"""tt2 = tt.index.tolist()
tt.reset_index(inplace=True)"""
tt2 = tt[['출발영업소명','도착영업소명']]
tt2.head()
tt2 = tt2.set_index(['출발영업소명','도착영업소명'])
tt2 = tt2.index.tolist()
for i1, i2 in tt2:
    if idx%100 ==0:
        print(idx, '출발영업소 ',i1, '// 도착영업소',i2)
    temp_cityname= None
    temp_provname= None
    temp_tollname= None
    jdx1 = 0
    for j in df_province.지명:
        if (Series(i1).str.contains(j).astype('int32').sum()==1) :
            temp_cityname = j
            temp_tollname = i1
            temp_provname = df_province.도명[jdx1]
            break
        jdx1+=1
    dp_city.append(temp_cityname)
    dp_prov.append(temp_provname)
    dp_toll.append(temp_tollname)

    temp_cityname= None
    temp_provname= None
    temp_tollname= None
    jdx2 = 0
    for j in df_province.지명:
        if (Series(i2).str.contains(j).astype('int32').sum()==1) :
            temp_cityname = j
            temp_tollname = i2
            temp_provname = df_province.도명[jdx2]
            break
        jdx2+=1
    ar_city.append(temp_cityname)
    ar_prov.append(temp_provname)
    ar_toll.append(temp_tollname)
    idx+=1

df_dp_ar_TollCityProv = DataFrame([dp_toll, dp_city,dp_prov, ar_toll, ar_city,ar_prov]).T
df_dp_ar_TollCityProv.columns=['출발영업소명','출발시명','출발도명','도착영업소명','도착시명','도착도명']
df_dp_ar_TollCityProv.to_pickle('toll_city_prov_dataframe.pkl')


ddd = pd.read_pickle('C:\\Python_workdir\\finalproj\\toll_city_prov_dataframe.pkl')
df_dp_ar_TollCityProv_dropna =  ddd.dropna()
df_dp_ar_TollCityProv_dropna.info()

import time
#2019 1-12, 2020 1-12, 2021 1-10
for ifiles in range(34):
    suffix_name = str(int(ifiles/12)+2019)+'_'+str(int(ifiles%12)+1).zfill(2)+'.pkl'

    monthlydata = pd.read_pickle('C:\\Python_workdir\\finalproj\\ex_traffic_'+suffix_name)
    monthlydata['집계일자'] = monthlydata['집계일자'].astype('str')
    monthlydata['집계일자'] = pd.to_datetime(monthlydata['집계일자'],format='%Y-%m-%d')
    monthlydata.info()
    dates = monthlydata.집계일자.unique().tolist()

    monthly_merge = DataFrame()

    for i in dates:
        print(pd.to_datetime(i,format='%Y-%m-%d'), ' 집계중...')
        temp = monthlydata['집계일자']==pd.to_datetime(i,format='%Y-%m-%d')
        dailydata = monthlydata.loc[temp,]
        
        daily_merge2 = pd.merge(dailydata,df_dp_ar_TollCityProv_dropna, how='inner', left_on=['출발영업소명','도착영업소명'], right_on = ['출발영업소명','도착영업소명'] ).groupby(['출발도명','도착도명'])[['출발도명','도착도명','도착지방향1종교통량','도착지방향2종교통량','도착지방향3종교통량','출발지방향1종교통량','출발지방향2종교통량','출발지방향3종교통량']].sum()
        daily_merge2.reset_index(inplace=True)

        daily_merge1 = DataFrame({'집계일자':[pd.to_datetime(i,format='%Y-%m-%d') for j in range(len(daily_merge2))]})
        
        daily_merge =pd.concat([daily_merge1, daily_merge2], axis=1)

        monthly_merge = monthly_merge.append(daily_merge, ignore_index=True)
        
    monthly_merge.to_pickle('C:\\Python_workdir\\finalproj\\ex_traffic_daily_merge_province_'+suffix_name)


yearlydata = DataFrame()
i=0
for i in range(34):
    suffix_name = str(int(i/12)+2019)+'_'+str(int(i%12)+1).zfill(2)+'.pkl'
    
    monthlydata = pd.read_pickle('C:\\Python_workdir\\finalproj\\ex_traffic_daily_merge_province_'+suffix_name)
    print(str(int(i/12)+2019)+'_'+str(int(i%12)+1).zfill(2)+' 진행중..')
    
    yearlydata = yearlydata.append(monthlydata,ignore_index=True)
    if (i%12==11 or i==max(range(34))):
        yearlydata.to_pickle('C:\\Python_workdir\\finalproj\\ex_traffic_daily_province_merge_'+str(int(i/12)+2019)+'.pkl')
        yearlydata = DataFrame()

test = pd.read_pickle('C:\\Python_workdir\\finalproj\\ex_traffic_daily_province_merge_2021.pkl')
test.info()
test.head()