import pandas as pd
import datetime as dt
import bs4, requests
import numpy as np

def NASDAQCOM():
    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader as web
    end = dt.date.today()
    start = end - dt.timedelta(730)
    NASDAQ = web.DataReader('NASDAQCOM', 'fred', start, end).dropna()
    NASDAQ['Date'] = NASDAQ.index
    NASDAQ.index = range(len(NASDAQ))
    NASDAQ = NASDAQ[NASDAQ.columns.tolist()[::-1]]
    NASDAQ['% Change'] = NASDAQ['NASDAQCOM'].pct_change() * 100
    return NASDAQ

def movers():
    response = requests.get('http://markets.businessinsider.com/index/market-movers/nasdaq_100')
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    tables = soup.findAll('table', class_='table')
    columns = ['Stock', 'Close', 'Chg', '% Chg']
    df1 = pd.DataFrame(columns=columns)
    for i, tr in enumerate(tables[0].findAll('tr')[1:11]):
        td = tr.findAll('td')
        name = td[0].text.strip()
        if len(name) > 20:
            name = name[:20]
        df1.loc[i, 'Stock'] = name
        chork = td[1].text.strip().split('\r\n')
        #f1.loc[i, 'Previous Close'] = chork[0]
        df1.loc[i, 'Close'] = chork[1]
        df1.loc[i, 'Chg'] = '+' + td[4].findAll('span')[0].text
        df1.loc[i, '% Chg'] = '+' + td[4].findAll('span')[1].text
        #df1.loc[i, '3M'] = td[7].findAll('span')[1].text
        #df1.loc[i, '6M'] = td[8].findAll('span')[1].text
        #df1.loc[i, '12M'] = td[9].findAll('span')[1].text
    df2 = pd.DataFrame(columns=columns)

    for i, tr in enumerate(reversed(tables[1].findAll('tr')[1:11])):
        td = tr.findAll('td')
        name = td[0].text.strip()
        if len(name) > 20:
            name = name[:20]
        df2.loc[i, 'Stock'] = name
        chork = td[1].text.strip().split('\r\n')
        #df2.loc[i, 'Previous Close'] = chork[0]
        df2.loc[i, 'Close'] = chork[1]
        df2.loc[i, 'Chg'] = td[4].findAll('span')[0].text
        df2.loc[i, '% Chg'] = td[4].findAll('span')[1].text
        #df2.loc[i, '3M'] = td[7].findAll('span')[1].text
        #df2.loc[i, '6M'] = td[8].findAll('span')[1].text
        #df2.loc[i, '12M'] = td[9].findAll('span')[1].text

    return df1, df2

def daily_stats():
    response = requests.get('https://www.nasdaq.com/aspx/DailyMarketStatistics.aspx#nasdaq_15_most_active_dollar')
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    dic = {}
    dic['Volume'] = soup.findAll('table', class_='body1')[2].findAll('td')[1].text
    chork = ['New Highs', 'New Lows', 'Advances', 'Declines', 'Unchanged', 'Total']
    for i, x in enumerate(soup.findAll('table', class_='body1')[3].findAll('tr')[:6]):
        dic[chork[i]] = int(x.findAll('td')[1].text.replace(',', ''))
    dic['A/D'] = '{0:.3f}'.format((dic['Advances'] / dic['Declines']))
    dic['Highs/Lows'] = '{0:.3f}'.format(dic['New Highs'] / dic['New Lows'])
    return dic

def n_days_ago(df, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.date.today())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df['date']), key=lambda d:abs(d-z))
    for i in df.index:
        if df.loc[i, 'date'] == closest:
            p = i
    return p

def faang():
    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader as web
    dic = {}
    for symbol in ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']:
        df = web.DataReader(symbol, 'iex',  (dt.date.today() - dt.timedelta(365)), dt.date.today()).reset_index()
        df = df[df.volume != 0]
        df['date'] = pd.to_datetime(df['date'])
        dic[symbol] = {}
        dic[symbol]['Close'], dic[symbol]['Volume'] = float(df['close'].iloc[-1]), "{:,}".format(int(df['volume'].iloc[-1]))
        dic[symbol]['7D'] = "{0:.2%}".format(((df['close'].iloc[-1] / df['close'].loc[n_days_ago(df, 7)]) - 1))
        dic[symbol]['30D'] = "{0:.2%}".format(((df['close'].iloc[-1] / df['close'].loc[n_days_ago(df, 30)]) - 1))
        dic[symbol]['90D'] = "{0:.2%}".format(((df['close'].iloc[-1] / df['close'].loc[n_days_ago(df, 90)]) - 1))
        days = (df['date'].iloc[-1] - pd.Timestamp(df['date'].iloc[-1].year, 1, 1)).days + 1
        dic[symbol]['YTD'] = "{0:.2%}".format(((df['close'].iloc[-1] / df['close'].loc[n_days_ago(df, days)]) - 1))
        #print(df.loc[n_days_ago(df, days)])   #check this
        dic[symbol]['1Y'] = "{0:.2%}".format(((df['close'].iloc[-1] / df['close'].loc[n_days_ago(df, 365)]) - 1))
    return dic



