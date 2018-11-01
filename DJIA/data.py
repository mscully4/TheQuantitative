import pandas as pd
import datetime as dt
import bs4, requests
import os

os.chdir('/home/daily_reports/DJIA/')

def DJIA():
    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader as web
    end = dt.date.today()
    start = end - dt.timedelta(730)
    DJIA = web.DataReader('DJIA', 'fred', start, end).dropna()
    DJIA['Date'] = DJIA.index
    DJIA.index = range(len(DJIA))
    return DJIA

def weights():
    weights = []
    url = 'http://indexarb.com/indexComponentWtsDJ.html'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.findAll("table", {"border":"0", "cellpadding":"1", "cellspacing":"0"})[1]
    rows = table.findAll(class_="left")[1:] 
    [weights.append((row.text.strip('\xa0'), float(list(row.next_siblings)[1].text))) for row in rows]
    return weights

def components():
    url = 'http://money.cnn.com/data/dow30/'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.findAll('table', class_="wsod_dataTable wsod_dataTableBig")[0]
    header = [x.text for x in table.findAll('th')]
    df = pd.DataFrame(columns=header)
    rows = table.findAll('tr')[1:]
    for i, row in enumerate(rows):
        td = row.findAll('td')
        for x, element in enumerate(td):
            df.loc[i, header[x]] = element.text
    companies = [name.split(u'\xa0', 1)[1] for name in list(df['Company'])]
    companies = [company[:15] if len(company) > 15 else company for company in companies]
    tickers = [name.split(u'\xa0', 1)[0] for name in list(df['Company'])]
    change = [float(x.strip('+')) for x in list(df['Change'])]
    per_change = [float(x.strip('+').strip('%')) for x in list(df['% Change'])]
    df['Change'] = change
    df['Company'] = companies
    df['% Change'] = per_change
    df.insert(loc=1, column="Ticker", value=tickers)
    w = weights()
    for i in range(30):
        df.loc[i, 'Weight'] = w[i][1]
    df.rename(columns={'YTDchange': 'YTD Change'}, inplace=True)
    df = df.sort_values('% Change', ascending=False)
    df = df.drop('Volume', axis=1)
    return df

def n_days_ago(df, n):
    #Gathering the data from a year ago
    x = pd.Timestamp(dt.datetime.now())
    z = x - pd.Timedelta(n, unit='d')
    closest = min(list(df['Date']), key=lambda d:abs(d-z))
    for i in range(len(df)):
        if df.loc[i, 'Date'] == closest:
            p = i
    return p

def performance(df):
    print("GATHERING DATA...")
    dic = {}
    dic['7D'] = "{0:.2%}".format(((df['DJIA'].iloc[-1] / df['DJIA'].loc[n_days_ago(df, 7)]) - 1))
    dic['30D'] = "{0:.2%}".format(((df['DJIA'].iloc[-1] / df['DJIA'].loc[n_days_ago(df, 30)]) - 1))
    dic['90D'] = "{0:.2%}".format(((df['DJIA'].iloc[-1] / df['DJIA'].loc[n_days_ago(df, 90)]) - 1))
    days = (df['Date'].iloc[-1] - pd.Timestamp(df['Date'].iloc[-1].year, 1, 1)).days + 1
    dic['YTD'] = "{0:.2%}".format(((df['DJIA'].iloc[-1] / df['DJIA'].loc[n_days_ago(df, days)]) - 1))
    #print(df.loc[n_days_ago(df, days)])   #check this
    dic['1Y'] = "{0:.2%}".format(((df['DJIA'].iloc[-1] / df['DJIA'].loc[n_days_ago(df, 365)]) - 1))
    return dic

##with pd.option_context('display.max_rows', None, 'display.max_columns', 20):
##    print(df)
