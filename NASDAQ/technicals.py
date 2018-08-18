import pandas as pd
import numpy as np
import os
import datetime as dt

#os.chdir('C:/Users/Michael/Documents/Files/Coding Projects/Bond Yields')

def n_days_ago(df, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in df.index:
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

def technicals(df):
    technicals  = {}
    year = df.tail(len(df) - n_days_ago(df, 365))
    technicals['range'] = (year['NASDAQCOM'].min(), year['NASDAQCOM'].max())
    technicals['7D Chg'] = ((float(df['NASDAQCOM'][-1:]) / df.loc[n_days_ago(df, 7), 'NASDAQCOM']) - 1)
    technicals['30D Chg'] = ((float(df['NASDAQCOM'][-1:]) / df.loc[n_days_ago(df, 30), 'NASDAQCOM']) - 1)
    technicals['90D Chg'] = ((float(df['NASDAQCOM'][-1:]) / df.loc[n_days_ago(df, 30), 'NASDAQCOM']) - 1)
    days = (df['Date'].iloc[-1] - pd.Timestamp(df['Date'].iloc[-1].year, 1, 1)).days
    technicals['YTD Chg'] = ((float(df['NASDAQCOM'][-1:]) / df.loc[n_days_ago(df, days), 'NASDAQCOM']) - 1)
    technicals['1Y Chg'] = ((float(df['NASDAQCOM'][-1:]) / df.loc[n_days_ago(df, 365), 'NASDAQCOM']) - 1)
    for item in technicals:
        if item != "range":
            technicals[item] = '{0:.2%}'.format(technicals[item])
    return technicals

def moving_averages(df):
    df_MA = pd.DataFrame(dtype=np.float64)
    df_MA['Date'] = df['Date']
    df_MA['NASDAQ'] = list(df['NASDAQCOM'])
    df_MA['50 Day MA'] = df_MA['NASDAQ'].rolling(50).mean()
    df_MA['100 Day MA'] = df_MA["NASDAQ"].rolling(100).mean()
    df_MA['200 Day MA'] = df_MA["NASDAQ"].rolling(200).mean()
    df_MA['50 Day EWMA'] = pd.Series.ewm(df_MA['NASDAQ'], span=50, min_periods=50).mean()
    df_MA['100 Day EWMA'] = pd.Series.ewm(df_MA['NASDAQ'], span=100, min_periods=100).mean()
    df_MA['200 Day EWMA'] = pd.Series.ewm(df_MA['NASDAQ'], span=200, min_periods=200).mean()
    return df_MA.tail(len(df_MA) - n_days_ago(df_MA, 365))

def bollinger_bands(df):
    df_bb = pd.DataFrame()
    df_bb['Date'] = df['Date']
    df_bb['NASDAQ'] = df['NASDAQCOM']
    df_bb['30 Day MA'] = df_bb['NASDAQ'].rolling(window=20).mean()
    df_bb['30 Day STD'] = df_bb['NASDAQ'].rolling(window=20).std()
    df_bb['Upper Band'] = df_bb['30 Day MA'] + (2 * df_bb['30 Day STD'])
    df_bb['Lower Band'] = df_bb['30 Day MA'] - (2 * df_bb['30 Day STD'])
    return df_bb.tail(len(df_bb) - n_days_ago(df_bb, 365))