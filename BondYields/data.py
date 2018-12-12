import pandas as pd
import numpy as np
import datetime as dt
import requests
import bs4
import xmltodict

pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web

#df = web.DataReader(["DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"], "fred", dt.date.today() - dt.timedelta(365), dt.date.today()))
def DGS10():
    DGS10 = web.DataReader(['DGS10'], 'fred', dt.date.today() - dt.timedelta(730), dt.date.today()).reset_index().dropna()
    return DGS10

def T10YIE():
    T10YIE = web.DataReader(['T10YIE'], 'fred', dt.date.today() - dt.timedelta(365), dt.date.today()).reset_index().dropna()
    return T10YIE

def T10Y2Y():
    T10Y2Y = web.DataReader(["T10Y2Y"], 'fred', dt.date.today() - dt.timedelta(365), dt.date.today()).reset_index().dropna()
    return T10Y2Y

def yields():
    columns = ["Date", "1M", "2M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
    df = pd.DataFrame(columns=columns)
    url = "http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20{}".format(dt.datetime.now().year)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    content = soup.findAll('content')[-20:]
    for i, line in enumerate(content[:20]):
        part = line.text.strip('\n\n').split('\n')[1:-1]
        for z, y in enumerate(part):
            if z == 0:
                df.loc[i, columns[z]] = pd.Timestamp(part[z].split('T')[0])
            else:
                if part[z] != '':
                    df.loc[i, columns[z]] = float(part[z])
                else:
                    df.loc[i, columns[z]] = np.nan
    return df

def n_days_ago(df, column, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.date.today())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df[column]), key=lambda d:abs(d-z))
    for i in df.index:
        if df.loc[i, column] == closest:
            p = i
    return p

def year_ago(df):
    columns = ["Date", "1M", "2M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
    year_ago = pd.DataFrame()
    date = df.iloc[-1]['Date']
    url = "http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20{}".format(dt.datetime.now().year - 1)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    content = soup.findAll('content')
    for i, line in enumerate(content):
        part = line.text.strip('\n\n').split('\n')[1:-1]
        for z, y in enumerate(part):
            if z == 0:
                year_ago.loc[i, columns[z]] = pd.Timestamp(part[z].split('T')[0])
            else:
                if y != "":
                    year_ago.loc[i, columns[z]] = float(part[z])
                else:
                    year_ago.loc[i, columns[z]] = np.nan
    return np.array(year_ago.loc[n_days_ago(year_ago, 'Date', 365)])[1:]
