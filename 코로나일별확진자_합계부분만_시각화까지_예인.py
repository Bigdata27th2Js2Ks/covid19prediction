

# 코로나 일별 확진자 - (지역합계) 665행
# 해당 데이터 가공 및 간단한 시각화해보기

file = open('c:/data/Covid_total_daily.csv', 'rb')  # rb : 바이너리(b) 형태로 read(r)
Covid_total_daily = pickle.load(file)          
file.close()


Covid_total_daily.info()

# 년도별로 묶어보기
year = Covid_total_daily.groupby(Covid_total_daily['standard_date'].dt.year).sum()

# 년도별 월별로 묶어보기
Covid_total_daily_2020 = Covid_total_daily[Covid_total_daily['standard_date'].dt.year == 2020]
Covid_total_daily_2021 = Covid_total_daily[Covid_total_daily['standard_date'].dt.year == 2021]

Covid_total_daily_2020   # 2020년도
Covid_total_daily_2021   # 2021년도

# 2020년도의 월별
monthly_2020 = Covid_total_daily_2020.groupby(Covid_total_daily_2020['standard_date'].dt.month).sum()

# 2021년도의 월별
monthly_2021 = Covid_total_daily_2021.groupby(Covid_total_daily_2021['standard_date'].dt.month).sum()

monthly_2020
monthly_2021


# 시각화 해보기
import matplotlib.pylab as plt

from matplotlib import font_manager,rc
font_name = font_manager.FontProperties(fname='c:/windows/fonts/malgun.ttf').get_name()
rc('font', family=font_name)


# 2020년도의 월별 데이터로 시각화해보기
plt.subplot(1,2,1)

plt.title('2020년도 월별', fontweight='bold', size = 20, color = 'black')
plt.plot(monthly_2020.index, monthly_2020.confirmed_cnt_daily, label='확진자 수', c='red')
plt.plot(monthly_2020.index, monthly_2020.death_cnt_daily, label='사망자 수', c='black')
plt.plot(monthly_2020.index, monthly_2020.isol_clear_cnt_daily, label='격리해제 수', c='green')
plt.xlabel('월별')
plt.ylabel('인원수(명)')
plt.legend()


# 2021년도의 월별 데이터로 시각화해보기
plt.subplot(1,2,2)
plt.title('2021년도 월별', fontweight='bold', size = 20, color = 'black')
plt.plot(monthly_2021.index, monthly_2021.confirmed_cnt_daily, label='확진자 수', c='red')
plt.plot(monthly_2021.index, monthly_2021.death_cnt_daily, label='사망자 수', c='black')
plt.plot(monthly_2021.index, monthly_2021.isol_clear_cnt_daily, label='격리해제 수', c='green')
plt.xlabel('월별')
plt.ylabel('인원수(명)')
plt.legend()
