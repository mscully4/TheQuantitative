import time
import pandas as pd
import os

os.chdir('/home/daily_reports/Bond Yields')

def moving_averages(df):
    print('ANALYZING DATA...')
    df_MA = pd.DataFrame()
    df_MA['Date'] = df['Date']
    df_MA['10Y 50 Day MA'] = df["10 yr"].rolling(50).mean()
    df_MA['10Y 100 Day MA'] = df["10 yr"].rolling(100).mean()
    df_MA['10Y 200 Day MA'] = df["10 yr"].rolling(200).mean()
    df_MA['10Y 50 Day EWMA'] = pd.Series.ewm(df['10 yr'], span=50, min_periods=50).mean()
    df_MA['10Y 100 Day EWMA'] = pd.Series.ewm(df['10 yr'], span=100, min_periods=100).mean()
    df_MA['10Y 200 Day EWMA'] = pd.Series.ewm(df['10 yr'], span=200, min_periods=200).mean()
    return df_MA

