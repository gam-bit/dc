# 국경일 : getHoliDeInfo
# 공휴일 : getRestDeInfo

import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd

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

