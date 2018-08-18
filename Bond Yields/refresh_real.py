import pandas as pd
import requests
import bs4
import time
import datetime
import os

os.chdir('/home/daily_reports/Bond Yields/')

def refresh():
    print('GATHERING DATA..')
    filename = '/home/daily_reports/Bond Yields/dataR.csv'
    df = pd.read_csv(filename, parse_dates=['DATE'], dtype=float)
    url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyield"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    dates = soup.findAll('td', class_="text_view_data", attrs={"scope":"row"})[::-1]
    new = 0
    for date in dates:
        if pd.Timestamp(date.text) not in list(df['DATE']):
            new += 1

    if new < len(dates):
        columns = list(df.columns)
        length = len(df)
        entries = soup.findAll('td', class_="text_view_data")
        z = -1
        for i in range((len(dates) - new) * 6, len(dates) * 6):
            if i % 6 == 0:
                z += 1
            try:
                df.loc[length + z, columns[i%6]] = float(entries[i].text)
            except ValueError:
                df.loc[length + z, columns[i%6]] = pd.Timestamp(entries[i].text)
                
    elif new == len(dates):
        year = datetime.datetime.now().year
        while True:
            url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyieldYear&year={}'.format(year)
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            dates = soup.findAll('td', class_="text_view_data", attrs={"scope":"row"})[::-1]
            new = 0
            #Note to self: change this to check only the last date rather than going through the entire list
            for date in dates:
                if pd.Timestamp(date.text) not in list(df['DATE']):
                    new += 1

            if new < len(dates):
                if new == 0:
                    year += 1
                    url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyieldYear&year={}".format(year)
                    response = requests.get(url)
                    soup = bs4.BeautifulSoup(response.text, 'lxml')
                columns = list(df.columns)
                length = len(df)
                entries = soup.findAll('td', class_="text_view_data")
                z = -1
                for i in range((len(dates) - new) * 6, len(dates) * 6):
                    if i % 6 == 0:
                        z += 1
                    try:
                        df.loc[length + z, columns[i%6]] = float(entries[i].text)
                    except ValueError:
                        df.loc[length + z, columns[i%6]] = pd.Timestamp(entries[i].text)
                        
                while year < datetime.datetime.now().year:
                    print(year, df.tail(30))
                    entries = soup.findAll('td', class_= "text_view_data")
                    length = len(df)
                    r = -1
                    for i in range(int(len(entries))):
                        if i % 6 == 0:
                            r += 1
                        try:
                            df.loc[length + r, columns[i % 6]] = float(entries[i].text)
                        except TypeError:
                            df.loc[length + r, columns[i % 6]] = pd.Timestamp(entries[i].text)
                    
                    year += 1
                    url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyieldYear&year={}".format(year)
                    response = requests.get(url)
                    soup = bs4.BeautifulSoup(response.text, 'lxml')
                break
            elif new == len(dates):
                print("even further")
            year -= 1
            
    elif not new:
        print("No need")


    df.to_csv(filename, index=False)


        


