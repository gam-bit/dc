# 국경일 : getHoliDeInfo
# 공휴일 : getRestDeInfo

import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# holiday_csv 파일 만드는 함수
def make_holiday_csv(years_lst=[2018, 2019, 2020, 2021], filename='C:/Users/km_mz/Desktop/dacon/daconcup/Data/holiday.csv'):

    data_lst = []
    for year in years_lst:
        url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
        key = '17I1VrbpvNWc3k7fYlMTRowquqx%2BvsNwUWykYKqhmpX6jHhbDsIjhgYaq5UARFaZLTkQ7o75H%2BC%2FCfOHKMaLcA%3D%3D'
        query = f"?solYear={year}&ServiceKey={key}&_type=json&numOfRows={100}"
        endpoint = url + query
        res = requests.get(endpoint)
        data = json.loads(res.text)['response']['body']['items']['item']
        data_lst += data

    with open(filename, 'w', newline='') as f:

        cols = ['dateKind', 'dateName', 'isHoliday', 'locdate', 'seq']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in data_lst:
            writer.writerow(row)

    print("Done making holiday.csv...")


def make_holiday_df(years_lst=[2018, 2019, 2020, 2021]):

    data_lst = []
    for year in years_lst:
        url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
        key = '17I1VrbpvNWc3k7fYlMTRowquqx%2BvsNwUWykYKqhmpX6jHhbDsIjhgYaq5UARFaZLTkQ7o75H%2BC%2FCfOHKMaLcA%3D%3D'
        query = f"?solYear={year}&ServiceKey={key}&_type=json&numOfRows={100}"
        endpoint = url + query
        res = requests.get(endpoint)
        data = json.loads(res.text)['response']['body']['items']['item']
        data_lst += data

    cols = ['dateKind', 'dateName', 'isHoliday', 'date', 'seq']
    df = pd.DataFrame(data_lst, columns = cols)

    return df




# pandas에 공휴일 칼럼 추가하는 함수
def add_isHoliday_column(df_having_date):
    holiday = make_holiday_df()
    holiday.columns = ['dateKind', 'dateName', 'isHoliday', 'date', 'seq']
    holiday['date'] = pd.to_datetime(holiday['date'])
    df = pd.merge(df_having_date, holiday[['date', 'isHoliday']], on='date', how='left')
    df['isHoliday'] = df.apply(lambda x: 1 if (x['date'].dayofweek == 5)|(x['date'].dayofweek == 6) | (x['isHoliday'] == 'Y') else 0, axis=1)
    
    return df



# train 데이터 날짜별 데이터로 바꾸기
def train_prep(df):
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['date'] = df.DateTime.dt.date
    df = df.groupby('date').sum().reset_index()
    return df

# 데이터 날짜별 count 데이터프레임으로 바꾸기
def info_prep(df, col='count'):
    # date 변수 추출
    df['c_time'] = pd.to_datetime(df['c_time'])
    df['date'] = df['c_time'].dt.date
    
    # missing value 제거
    df = df.dropna(how='all') # 모든 row가 missing value 일 때

    df = df.groupby('date')['date'].count().to_frame(name=col).reset_index()
    return df


# 날짜별 히트맵 
def check_date(df, title=''):
    """
    input:
    > 'date', '원하는 count' 두 칼럼으로 이루어진 df
    """

    import seaborn as sns
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df.apply(lambda x: x['date'].strftime('%Y') + '-' + x['date'].strftime('%m'), axis=1)
    df['day'] = df['date'].dt.strftime('%d')

    df_pivot = pd.pivot_table(df, index='year_month', columns='day', values=df.columns[1])
    fig = plt.figure(figsize=(15, 10))
    sns.heatmap(df_pivot, annot=True, fmt='.0f', cmap='YlGn',  linewidths=.1, linecolor='lightgrey')
    plt.title(f"<{title}>")
    plt.show();


#----------------

# 대회 참가자 수 넣기 -- 변형해서 쓰세요
def info_cpt_prep(data):
    
    # 날짜는 날짜형태로 변경
    data['period_start'] = pd.to_datetime(data['period_start'])
    data['period_end'] = pd.to_datetime(data['period_end'])
    data['merge_deadline'] = pd.to_datetime(data['merge_deadline'])

    # 날짜별 시행 대회 수
    min_date = min(data['period_start'])
    max_date = max(data['period_end'])
    cnt_cpt_df = pd.DataFrame()
    cnt_cpt_df['date'] = pd.date_range(min_date, max_date)
    for idx, row in data.iterrows():
        date_interval = pd.date_range(row['period_start'].date(), row['period_end'].date())
        col_name = row['name']
        
        cnt_cpt_df[col_name] = 0
        cnt_cpt_df.loc[cnt_cpt_df['date'].apply(lambda x: x in date_interval), col_name] = row['participants']

    cnt_cpt_df['total_participants'] = np.sum(cnt_cpt_df.iloc[:, 1:], axis=1)

    return cnt_cpt_df # date | name(대회이름)s | total_participants
    



# def train_preprocess(data, cnt_cpt_df):

#     # 일별 데이터 생성
#     data['date'] = pd.to_datetime(data['DateTime'].apply(lambda x: x[:10]))
#     df = data.groupby('date')[['사용자', '세션', '신규방문자', '페이지뷰']].sum()
#     y_cols = ['y_user', 'y_sess', 'y_new', 'y_views']
#     df.columns = y_cols
#     df = df.reset_index()
#     # print(df.info())

#     # 공휴일 여부 추가
#     df = utils.add_isHoliday_column(df)


#     # lag1~14변수 생성
#     for col in y_cols:
#         for i in range(1, 15): 
#             col_name = col[2:] + '_lag' + str(i)
#             df[col_name] = df[col].shift(i)

#     # lag 변수들의 분산, 평균, 중앙값
#     for col in y_cols:
#         factor = col[2:]
#         new_cols = [factor+'_lag_mean', factor+'_lag_std']
#         df[new_cols] = df[[col for col in df if col.startswith(factor)]].apply(pd.DataFrame.describe, axis=1)[['mean', 'std']]

#     # 대회 참가자 수
#     df = df.merge(cnt_cpt_df.loc[:, ['date', 'total_participants']], on='date', how='left')

#     return df
#--------------------------------------------------------------