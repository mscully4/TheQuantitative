#!/usr/bin/env python3

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import datetime as dt
import numpy as np
import matplotlib.dates as mdates
import os

os.chdir('/home/daily_reports/FX/')

def year_ago(df):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(365, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in range(len(df)):
        if df.loc[i, 'Date'] == closest:
            p = i
    year = list(df.loc[p])[1:12]
    return p

def plot_developed_currencies(df):
    print("GENERATING GRAPHS.")
    fig = plt.figure()
    df = df.tail(len(df) - year_ago(df))
    dates = np.array(df['Date'])
    original = np.array(df.loc[df.index[0]][1:])
    price_change = df.drop(df.columns[0], axis=1).diff().cumsum()
    percent_change = (price_change / original)
    plt.plot(dates, percent_change['(EUR)'], color='b')
    plt.plot(dates, percent_change['(GBP)'], color='r')
    plt.plot(dates, percent_change['(JPY)'], color='#000000')
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.suptitle('Developed Economies against the Dollar YTD')
    plt.ylabel("Percent Change")
    plt.legend(['Euro', 'Pound', 'Yen'])
    plt.gca().grid(True)
    plt.gca().set_facecolor('#E2DED6')
    plt.subplots_adjust(top=0.93, bottom=0.06, left=0.12,
                        right=0.96, hspace=0.2, wspace=0.2)
    plt.savefig('DevelopedEconomiesYTD.png')
    return fig
    

def plot_emerging_currencies(df):
    print("GENERATING GRAPHS..")
    fig = plt.figure()
    df = df.tail(len(df) - year_ago(df))
    dates = np.array(df['Date'])
    original = np.array(df.loc[df.index[0]][1:])
    price_change = df.drop(df.columns[0], axis=1).diff().cumsum()
    percent_change = (price_change / original)
    plt.plot(dates, percent_change['(CNY)'], color='r')
    plt.plot(dates, percent_change['(INR)'], color='#fac205')
    plt.plot(dates, percent_change['(RUB)'], color='b')
    plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.suptitle('Emerging Economies against the Dollar YTD')
    plt.ylabel("Percent Change")
    plt.legend(['Yuan', 'Rupee', 'Ruble'])
    plt.gca().grid(True)
    plt.gca().set_facecolor('#E2DED6')
    plt.subplots_adjust(top=0.93, bottom=0.06, left=0.12,
                        right=0.96, hspace=0.2, wspace=0.2)
    plt.savefig('EmergingEconomiesYTD.png')
    return fig

def plot_trade_weighted_dollar():
    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader as web
    end = dt.date.today()
    start = end - dt.timedelta(730)
    DTWEXM = web.DataReader('DTWEXM', 'fred', start, end).dropna()
    DTWEXM = DTWEXM.reset_index()
    DTWEXM.columns = ['Date', 'DTWEXM']
    df = DTWEXM.tail(len(DTWEXM) - year_ago(DTWEXM))
    fig = plt.figure()
    plt.plot(df['Date'], df['DTWEXM'], color="black")
    plt.suptitle("Trade Weighted US Dollar Index")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    plt.gca().set_yticklabels(['{0:,.0f}'.format(x) for x in plt.gca().get_yticks()])
    fig.autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.gca().set_facecolor('#E2DED6')
    plt.legend()
    plt.subplots_adjust(top=0.92, bottom=0.1, left=0.08,
                                             right=0.98, hspace=0.2, wspace=0.2)
    fig.savefig("/home/daily_reports/FX/Trade Weighted Dollar.png")

from bollinger_bands import bollinger_bands, exponential_bollinger_bands

def plot_bollinger_bands(df, currency):
    df_MA = exponential_bollinger_bands(df, currency)
    df = df.tail(len(df) - year_ago(df))
    upper = np.array(df_MA['Upper Band'])
    lower = np.array(df_MA['Lower Band'])
    x = np.array(df_MA['Date'])
    plt.gca().fill_between(x, upper, lower, color='grey')
    plt.plot(df['Date'], df[currency], color="blue")
    plt.plot(df_MA['Date'], df_MA['30 Day EMA'], color="black")
    plt.show()

