import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import os

os.chdir('/home/daily_reports/Bond Yields/')

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

def yield_curve(df, year_ago):
    print('GENERATING GRAPHS.')
    #Plotting today's yield curve and last year's
    fig = plt.figure()
    plt.suptitle("Today vs a Year Ago")
    time = [(1/12), (1/6), (1/4), (1/2), 1, 2, 3, 5, 7, 10, 20, 30]
    today = list(df.iloc[-1])[1:]
    plt.plot(time, today, "-", color="000000")
    plt.ylabel("Yield")
    plt.xlabel("Maturity")
    plt.plot(time, year_ago, "-", color="blue")
    plt.legend(['Today', 'A Year Ago'])
    plt.xticks(time[3:])
    vals = plt.gca().get_yticks()
    #graph2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.gca().set_yticklabels(['{:1.1f}%'.format(x) for x in plt.gca().get_yticks()])
    plt.gca().set_xticklabels(plt.gca().get_xticks().astype(int))
    fig.autofmt_xdate()
    plt.subplots_adjust(top=0.915, bottom=0.13, left=0.12, right=0.95, hspace=0.21, wspace=0.2)
    plt.gca().set_facecolor('#E2DED6')
    plt.gca().yaxis.grid(True)
    fig.savefig("/home/daily_reports/Bond Yields/YearAgo.png")
    return fig

def yield_spread(df):
    print('GENERATING GRAPHS..')
    #Plotting the 10Y - 2Y spread
    fig = plt.figure()
    plt.suptitle('10Y - 2Y Yield Spread')
    plt.plot(df['DATE'], df['T10Y2Y'], color="black")
    plt.ylabel('Spread')
    plt.gca().set_yticklabels(['{:1.1f}%'.format(x) for x in plt.gca().get_yticks()])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    fig.autofmt_xdate()
    plt.grid(True)
    plt.subplots_adjust(top=0.915, bottom=0.13, left=0.12,
                        right=0.95, hspace=0.2, wspace=0.2)
    plt.gca().set_facecolor('#E2DED6')
    fig.savefig("YieldSpreads.png")
    return fig

def moving_averages(df_MA):
    print('GENERATING GRAPHS...')
    fig = plt.figure()
    plt.plot(df_MA['DATE'], df_MA['DGS10'], color="black")
    plt.plot(df_MA['DATE'], df_MA['10Y 50 Day MA'], color="green")
    plt.plot(df_MA['DATE'], df_MA['10Y 100 Day MA'], color="blue")
    plt.plot(df_MA['DATE'], df_MA['10Y 200 Day MA'], color="red")
    plt.suptitle("10yr Treasury w/ Moving Averages")
    plt.legend(['10 yr', '10Y 50 Day MA', '10Y 100 Day MA', '10Y 200 Day MA'])
    plt.ylabel('Rate')
    fig.autofmt_xdate()
    plt.grid(True)
    plt.gca().set_yticklabels(['{:1.1f}%'.format(x) for x in plt.gca().get_yticks()])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    plt.gca().set_facecolor('#E2DED6')
    plt.subplots_adjust(top=0.92, bottom=0.13,
                        left=0.12, right=0.95, hspace=0.2,
                        wspace=0.2)
    fig.savefig("MovingAverages.png")
    return fig

def exponential_moving_averages(df, df_MA):
    p = year_ago(df)
    df = df.tail(len(df) - p)
    df_MA = df_MA.tail(len(df_MA) - p)
    fig = plt.figure()
    plt.plot('Date', '10 yr', data=df, color="black")
    plt.plot('Date', '10Y 50 Day EWMA', data=df_MA, color="green")
    plt.plot('Date', '10Y 100 Day EWMA', data=df_MA, color="blue")
    plt.plot('Date', '10Y 200 Day EWMA', data=df_MA, color="red")
    plt.suptitle("10yr Treasury w/ Exponential Weighted Moving Averages")
    fig.autofmt_xdate()
    plt.grid(True)
    plt.gca().set_facecolor('#E2DED6')
    plt.gca().set_yticklabels(['{:1.1f}%'.format(x) for x in plt.gca().get_yticks()])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    plt.subplots_adjust(top=0.92, bottom=0.13,
                        left=0.12, right=0.95, hspace=0.2,
                        wspace=0.2)
    fig.savefig("ExponentialMovingAverages.png")
    return fig

def breakeven_rate(df):
    print('GENERATING GRAPHS....')
    fig = plt.figure()
    plt.suptitle('10YR Breakeven Rate')
    plt.plot(df['DATE'], df['T10YIE'], color="black")
    plt.ylabel('Breakeven Rate')
    fig.autofmt_xdate()
    plt.grid(True)
    plt.subplots_adjust(top=0.92, bottom=0.13, left=0.12, right=0.95, hspace=0.2, wspace=0.2)
    plt.gca().set_yticklabels(['{:1.1f}%'.format(x) for x in plt.gca().get_yticks()])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    plt.gca().set_facecolor('#E2DED6')
    fig.savefig("Breakeven Rate.png")
    return fig
