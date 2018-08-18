import data, technicals
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import datetime as dt
import os

os.chdir('/home/daily_reports/DJIA/')

def year_ago(df):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(365, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in range(len(df)):
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

##Dow Jones Indsutrial Index w/ Moving Averages

def DowJonesIndustrialAverageWBollingerBands(df):
    df_BB = technicals.bollinger_bands(df)
    df = df.tail(len(df) - year_ago(df))
    fig = plt.figure()
    #plt.plot(df_BB['Date'], df_BB['Lower Band'], color="#5B92DC")
    #plt.plot(df_BB['Date'], df_BB['Upper Band'], color="#5B92DC")
    #plt.fill_between(np.array(df_BB['Date']), np.array(df_BB['Upper Band']), np.array(df_BB['Lower Band']), facecolor='#5B92DC')
    plt.plot(df['Date'], df['DJIA'], color="black")
    plt.suptitle("Dow Jones Industrial Average")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    plt.gca().set_yticklabels(['{0:,.0f}'.format(x) for x in plt.gca().get_yticks()])
    fig.autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.gca().set_facecolor('#E2DED6')
    plt.subplots_adjust(top=0.92, bottom=0.1, left=0.14,
                        right=0.95, hspace=0.2, wspace=0.2)
    fig.savefig("DowJonesIndustrialAverage.png")
    plt.show()
    return fig
