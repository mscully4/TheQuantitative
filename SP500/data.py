import pandas as pd
import datetime as dt
import bs4, requests
import re
import os

os.chdir('/home/daily_reports/SP500/')

def n_days_ago(df, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.date.today())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in df.index:
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

def SP500():
    print("GATHERING DATA")
    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader as web
    end = dt.date.today()
    start = end - dt.timedelta(730)
    SP500 = web.DataReader('SP500', 'fred', start, end).dropna()
    SP500['Date'] = SP500.index
    SP500.index = range(len(SP500))
    SP500 = SP500[SP500.columns.tolist()[::-1]]
    return SP500

def quote_details():
    print("GATHERING DATA.")
    url = "http://money.cnn.com/data/markets/sandp/"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    dic = {}
    high_low = soup.find('table', class_="wsod_quoteData").find('td', class_="wsod_52week")
    dic['52 week range'] = (high_low.find(class_="val lo").text, high_low.find(class_="val hi").text)
    simple_data = soup.findAll('table', class_='wsod_dataTableBig')[1]
    for x in simple_data.findAll('tr'):
        dic[(x.findAll('td')[0]).text] = x.findAll('td')[1].text
    return dic

def ratios():
    print("GATHERING DATA..")
    dic = {}
    url1 = "http://www.multpl.com/"
    response = requests.get(url1)
    P2E = bs4.BeautifulSoup(response.text, 'lxml')
    dic['P2E'] = P2E.find('div', id="current").findAll('span')[1].previous_sibling.split()[0]
    url2 = "http://www.multpl.com/s-p-500-price-to-sales"
    response = requests.get(url2)
    P2R = bs4.BeautifulSoup(response.text, 'lxml')
    dic['P2R'] = P2R.find('div', id="current").findAll('span')[1].previous_sibling.split()[0]
    url3 = "http://www.multpl.com/s-p-500-price-to-book"
    response = requests.get(url3)
    P2B = bs4.BeautifulSoup(response.text, 'lxml')
    dic['P2B'] = P2B.find('div', id="current").findAll('span')[1].previous_sibling.split()[0]
    return dic

def performance(df):
    print("GATHERING DATA...")
    dic = {}
    dic['7D'] = "{0:.2%}".format(((df['SP500'].iloc[-1] / df['SP500'].loc[n_days_ago(df, 7)]) - 1))
    dic['30D'] = "{0:.2%}".format(((df['SP500'].iloc[-1] / df['SP500'].loc[n_days_ago(df, 30)]) - 1))
    dic['90D'] = "{0:.2%}".format(((df['SP500'].iloc[-1] / df['SP500'].loc[n_days_ago(df, 90)]) - 1))
    days = (df['Date'].iloc[-1] - pd.Timestamp(df['Date'].iloc[-1].year, 1, 1)).days + 1
    dic['YTD'] = "{0:.2%}".format(((df['SP500'].iloc[-1] / df['SP500'].loc[n_days_ago(df, days)]) - 1))
    #print(df.loc[n_days_ago(df, days)])   #check this
    dic['1Y'] = "{0:.2%}".format(((df['SP500'].iloc[-1] / df['SP500'].loc[n_days_ago(df, 365)]) - 1))
    return dic

def big_movers():
    print("GATHERING DATA....")
    url = "https://money.cnn.com/data/hotstocks/"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    tables = soup.findAll('table')
    active, gainers, losers = tables[0].findAll('tr'), tables[1].findAll('tr'), tables[2].findAll('tr')
    columns = ["Ticker", "Stock", "Price", "Change", "% Change"]
    r = re.compile(r'\bInc\b | \bCo\b | \bCorp\b', flags=re.I | re.X)
    df1 = pd.DataFrame(columns=columns)
    for z, stock in enumerate(active[1:]):
        d = stock.findAll('td')
        df1.loc[z, "Ticker"] = d[0].text.split(" ", 1)[0]
        for i in range(4):
            if i == 0:
                df1.loc[z, columns[i + 1]] = d[i].text.split(" ", 1)[1]
                name = d[i].text.split(" ", 1)[1]
                for suffix in r.findall(name.split(" ", 1)[1]):
                    name = re.sub(suffix, '', name)
                    if len(name) > 21:
                        name = name[:21]
                df1.loc[z, columns[i + 1]] = name
            else:
                df1.loc[z, columns[i + 1]] = d[i].text
    df2 = pd.DataFrame(columns=columns)
    for z, stock in enumerate(gainers[1:]):
        d = stock.findAll('td')
        df2.loc[z, "Ticker"] = d[0].text.split(" ", 1)[0]
        for i in range(4):
            if i == 0:
                df2.loc[z, columns[i + 1]] = d[i].text.split(" ", 1)[1]
                name = d[i].text.split(" ", 1)[1]
                for suffix in r.findall(name.split(" ", 1)[1]):
                    name = re.sub(suffix, '', name)
                    if len(name) > 21:
                        name = name[:21]
                df2.loc[z, columns[i + 1]] = name
            else:
                df2.loc[z, columns[i + 1]] = d[i].text
    df3 = pd.DataFrame(columns=columns)
    for z, stock in enumerate(losers[1:]):
        d = stock.findAll('td')
        df3.loc[z, "Ticker"] = d[0].text.split(" ", 1)[0]
        for i in range(4):
            if i == 0:
                df3.loc[z, columns[i + 1]] = d[i].text.split(" ", 1)[1]
                name = d[i].text.split(" ", 1)[1]
                for suffix in r.findall(name.split(" ", 1)[1]):
                    name = re.sub(suffix, '', name)
                    if len(name) > 21:
                        name = name[:21]
                df3.loc[z, columns[i + 1]] = name
            else:
                df3.loc[z, columns[i + 1]] = d[i].text
    for df in [df1, df2, df3]:
        df.columns = ['Ticker', 'Stock', 'Price', 'Chg.', '% Chg.']
    return df1, df2, df3
