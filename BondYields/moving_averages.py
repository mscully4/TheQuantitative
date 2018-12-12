import time
import pandas as pd
import datetime as dt
import os

os.chdir('/home/daily_reports/BondYields')

def n_days_ago(df, column, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.date.today())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df[column]), key=lambda d:abs(d-z))
    for i in df.index:
        if df.loc[i, column] == closest:
            p = i
    return p

def moving_averages(df):
    print('ANALYZING DATA...')
    df_MA = pd.DataFrame()
    df_MA['DATE'] = df['DATE']
    df_MA['DGS10'] = df['DGS10']
    df_MA['10Y 50 Day MA'] = df_MA["DGS10"].rolling(50).mean()
    df_MA['10Y 100 Day MA'] = df_MA["DGS10"].rolling(100).mean()
    df_MA['10Y 200 Day MA'] = df_MA["DGS10"].rolling(200).mean()
    df_MA['10Y 50 Day EWMA'] = pd.Series.ewm(df_MA['DGS10'], span=50, min_periods=50).mean()
    df_MA['10Y 100 Day EWMA'] = pd.Series.ewm(df_MA['DGS10'], span=100, min_periods=100).mean()
    df_MA['10Y 200 Day EWMA'] = pd.Series.ewm(df_MA['DGS10'], span=200, min_periods=200).mean()
    return df_MA.tail(n_days_ago(df_MA, 'DATE', 365))

