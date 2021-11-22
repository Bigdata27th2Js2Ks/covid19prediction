from datetime import timedelta
import pandas as pd
from pandas import DataFrame, Series
from pandas.core.reshape import reshape


#---매월 말일자료 만들어서 말일 이후의 NaN값 날리기 (e.g., 2월 30일,31일, 4월 31일..등)
seoul_temp_max = pd.read_csv('C:\\Python_workdir\\finalproj\\weather\\seoul_daily_temp_max.csv', encoding='cp949')

yrmonth = seoul_temp_max.columns.tolist()[:-1]
eod_monthly = [31,28,31,30,31,30, 31,31,30,31,30,31 ,
                31,29,31,30,31,30, 31,31,30,31,30,31 ,
                31,28,31,30,31,30, 31,31,30,31,30]

end_of_days_in_month = DataFrame(yrmonth, eod_monthly)
end_of_days_in_month.reset_index(inplace=True)
end_of_days_in_month.columns = ['말일','연월']
end_of_days_in_month=end_of_days_in_month[['연월','말일']]
end_of_days_in_month


loca = ['seoul','suwon','incheon']

for iloca in loca:
    #iloca = loca[0]
    # 1. 최고기온 자료 전처리
    temp_max = pd.read_csv('C:\\Python_workdir\\finalproj\\weather\\'+iloca+'_daily_temp_max.csv', encoding='cp949')

    temp_max.reset_index(inplace=True)
    temp_max_monthly = temp_max.iloc[-1]
    temp_max = temp_max.iloc[:-1,]
    daily_maxtemp =DataFrame(columns=['연월','일','최고기온'])
    #pd.to_datetime('2021-02-29',format='%Y-%m-%d')
    for i in temp_max.columns:
        #i=temp_max.columns[1]
        tempmonth = [i for j in range(len(temp_max[i]))]
        daily_maxtemp = pd.concat([daily_maxtemp, 
                DataFrame({'연월': tempmonth, '일':Series(temp_max.일자).str[:-1].astype('int32').tolist(), '최고기온':temp_max.loc[:,i].tolist()} )])

    daily_maxtemp = daily_maxtemp.reset_index()
    daily_maxtemp.columns

    #2 평균기온 자료
    temp_avg = pd.read_csv('C:\\Python_workdir\\finalproj\\weather\\'+iloca+'_daily_temp_avg.csv', encoding='cp949')

    temp_avg.reset_index(inplace=True)
    temp_avg_monthly = temp_avg.iloc[-1]
    temp_avg = temp_avg.iloc[:-1,]
    daily_avgtemp =DataFrame(columns=['연월','일','평균기온'])
    #pd.to_datetime('2021-02-29',format='%Y-%m-%d')
    for i in temp_avg.columns:
        #i=temp_avg.columns[1]
        tempmonth = [i for j in range(len(temp_avg[i]))]
        daily_avgtemp = pd.concat([daily_avgtemp, 
                            DataFrame({'연월': tempmonth, 
                            '일':Series(temp_avg.일자).str[:-1].astype('int32').tolist(), '평균기온':temp_avg.loc[:,i].tolist()} )])

    daily_avgtemp = daily_avgtemp.reset_index()

    #3 강수량 자료
    precipi = pd.read_csv('C:\\Python_workdir\\finalproj\\weather\\'+iloca+'_daily_precipitation.csv', encoding='cp949')

    precipi.reset_index(inplace=True)
    precipi_monthly = precipi.iloc[-1]
    precipi = precipi.iloc[:-1,]
    daily_precipi =DataFrame(columns=['연월','일','일강수량'])
    #pd.to_datetime('2021-02-29',format='%Y-%m-%d')
    for i in precipi.columns:
        #i=temp_avg.columns[1]
        try:
            tempmonth = [i for j in range(len(temp_avg[i]))]
            daily_precipi = pd.concat([daily_precipi, 
                                DataFrame({'연월': tempmonth, 
                                '일':Series(precipi.일자).str[:-1].astype('int32').tolist(), '일강수량':precipi.loc[:,i].tolist()} ) ])
        except:
            pass

    daily_precipi = daily_precipi.reset_index()

    # 제대로된 일자와 날씨자료 병합
    #1 최고기온
    daily_temp_max = pd.merge(end_of_days_in_month,daily_maxtemp, how='inner', left_on='연월', right_on='연월')[['연월','일','말일','최고기온']]

    daily_temp_max = daily_temp_max[daily_temp_max.일 <= daily_temp_max.말일]
    daily_temp_max['일시']=pd.to_datetime(daily_temp_max.연월 +'-'+ Series(daily_temp_max.일).astype('str').str.zfill(2), format='%Y-%m-%d')

    #2 평균기온
    daily_temp_avg = pd.merge(end_of_days_in_month,daily_avgtemp, how='inner', left_on='연월', right_on='연월')[['연월','일','말일','평균기온']]

    daily_temp_avg = daily_temp_avg[daily_temp_avg.일 <= daily_temp_avg.말일]
    daily_temp_avg['일시']=pd.to_datetime(daily_temp_avg.연월 +'-'+ Series(daily_temp_avg.일).astype('str').str.zfill(2), format='%Y-%m-%d')

    #3 강수량
    daily_precipi = pd.merge(end_of_days_in_month,daily_precipi, how='inner', left_on='연월', right_on='연월')[['연월','일','말일','일강수량']]

    daily_precipi = daily_precipi[daily_precipi.일 <= daily_precipi.말일]
    daily_precipi['일시']=pd.to_datetime(daily_precipi.연월 +'-'+ Series(daily_precipi.일).astype('str').str.zfill(2), format='%Y-%m-%d')


    # merge data
    daily_weather = pd.merge(daily_temp_max,daily_temp_avg,how='inner',left_on='일시',right_on='일시')[['일시','최고기온','평균기온']]
    
    daily_weather = pd.merge(daily_weather,daily_precipi,how='inner',left_on='일시',right_on='일시')[['일시','최고기온','평균기온','일강수량']]

    daily_weather.to_csv(iloca+'_daily_weather_201901-202111.csv',index=False)
    daily_weather.to_pickle(iloca+'_daily_weather_201901-202111.pkl')
    