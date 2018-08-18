import data, technicals
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import os

os.chdir('/home/daily_reports/SP500/')

def year_ago(df):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(365, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in range(len(df)):
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

def SP500(df):
    print("GENERATING PLOTS...")
    df_MA = technicals.moving_averages(df)
    df = df.tail(len(df) - year_ago(df))
    fig = plt.figure()
    plt.plot(df['Date'], df['SP500'], color="black")
    plt.plot(df_MA['Date'], df_MA['50 Day MA'], color="green")
    plt.plot(df_MA['Date'], df_MA['100 Day MA'], color="blue")
    plt.plot(df_MA['Date'], df_MA['200 Day MA'], color="red")
    plt.suptitle("S&P 500")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    plt.gca().set_yticklabels(['{0:,.0f}'.format(x) for x in plt.gca().get_yticks()])
    fig.autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.gca().set_facecolor('#E2DED6')
    plt.legend()
    plt.subplots_adjust(top=0.92, bottom=0.1, left=0.14,
                                             right=0.95, hspace=0.2, wspace=0.2)
    fig.savefig("/home/daily_reports/SP500/SP500.png")
    return fig
