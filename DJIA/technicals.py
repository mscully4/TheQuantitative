import data
import pandas as pd
import numpy as np
import os
import datetime as dt

os.chdir('/home/daily_reports/DJIA/')

def n_days_ago(df, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in range(len(df)):
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

def moving_averages(df):
    df_MA = pd.DataFrame(dtype=np.float64)
    df_MA['Date'] = df['Date']
    df_MA['DJIA'] = list(df['DJIA'])
    df_MA['50 Day MA'] = df_MA['DJIA'].rolling(50).mean()
    df_MA['100 Day MA'] = df_MA["DJIA"].rolling(100).mean()
    df_MA['200 Day MA'] = df_MA["DJIA"].rolling(200).mean()
    df_MA['50 Day EWMA'] = pd.Series.ewm(df_MA['DJIA'], span=50, min_periods=50).mean()
    df_MA['100 Day EWMA'] = pd.Series.ewm(df_MA['DJIA'], span=100, min_periods=100).mean()
    df_MA['200 Day EWMA'] = pd.Series.ewm(df_MA['DJIA'], span=200, min_periods=200).mean()
    return df_MA.tail(len(df_MA) - n_days_ago(df_MA, 365))

def bollinger_bands(df):
    df_bb = pd.DataFrame()
    df_bb['Date'] = df['Date']
    df_bb['DJIA'] = df['DJIA']
    df_bb['30 Day MA'] = df_bb['DJIA'].rolling(window=20).mean()
    df_bb['30 Day STD'] = df_bb['DJIA'].rolling(window=20).std()
    df_bb['Upper Band'] = df_bb['30 Day MA'] + (2 * df_bb['30 Day STD'])
    df_bb['Lower Band'] = df_bb['30 Day MA'] - (2 * df_bb['30 Day STD'])
    return df_bb.tail(len(df_bb) - n_days_ago(df_bb, 365))
