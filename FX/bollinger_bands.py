#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import os

os.chdir('/home/daily_reports/FX')

def year_ago(df):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(365, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in range(len(df)):
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

def bollinger_bands(df, currency):
    print("ANALYZING DATA...")
    df_MA = pd.DataFrame()
    df_MA['Date'] = df['Date']
    df_MA[currency] = df[currency]
    df_MA['30 Day MA'] = df_MA[currency].rolling(window=20).mean()
    df_MA['30 Day STD'] = df_MA[currency].rolling(window=20).std()
    df_MA = df_MA.tail(len(df_MA) - year_ago(df_MA))
    df_MA['Upper Band'] = df_MA['30 Day MA'] + (2 * df_MA['30 Day STD'])
    df_MA['Lower Band'] = df_MA['30 Day MA'] - (2 * df_MA['30 Day STD'])
    return df_MA.loc[df_MA.index[-1]]

def exponential_bollinger_bands(df, currency):
    df_EMA = pd.DataFrame()
    df_EMA['Date'] = df['Date']
    df_EMA[currency] = df[currency]
    df_EMA['30 Day EMA'] = pd.Series.ewm(df[currency], span=20).mean()
    df_EMA['30 Day STD'] = pd.Series.ewm(df[currency], span=20).std()
    df_EMA = df_EMA.tail(len(df_EMA) - year_ago(df_EMA))
    df_EMA['Upper Band'] = df_EMA['30 Day EMA'] + (2 * df_EMA['30 Day STD'])
    df_EMA['Lower Band'] = df_EMA['30 Day EMA'] - (2 * df_EMA['30 Day STD'])
    return df_EMA.loc[df_EMA.index[-1]]

def generate_bollinger_bands(df):
    currencies = list(df.columns)[2:]
    columns = ['Currency', 'Close', '30 Day MA', '30 Day STD', 'Upper Band', 'Lower Band']
    bands = pd.DataFrame(columns=columns)
    for i, currency in enumerate(currencies):
        data = list(bollinger_bands(df, currency))[1:]
        bands.loc[i, 'Currency'] = currency
        for x in range(len(data)):
            bands.loc[i, columns[x + 1]] = data[x]
    return bands.round(decimals=2)
