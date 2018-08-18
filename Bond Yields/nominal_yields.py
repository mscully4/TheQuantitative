import requests
import datetime
import json
import xmltodict
import pandas as pd
import numpy as np
import openpyxl as xl
import collections
import bs4
import time
import sqlite3
import os

os.chdir('/home/daily_reports/Bond Yields/')

###Scrapping All Data From The Treasury Website

url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'lxml')
headers = soup.findAll('th')
columns = []
for header in headers:
    columns.append(header.text)
entries = soup.findAll('td', class_="text_view_data")

df = pd.DataFrame(columns=columns)

length = len(entries)
z = -1

for q, entry in enumerate(entries):
    if q % 12 == 0:
        z += 1
    try:
        df.loc[z, columns[q % 12]] = float(entry.text)
    except ValueError:
        if entry.text == "\n\t\t\tN/A\n\t\t" or entry.text =="N/A":
            df.loc[z, columns[q % 12]] = None
        else:
            df.loc[z, columns[q % 12]] = pd.Timestamp(entry.text)

df.to_csv('/home/daily_reports/Bond Yields/data.csv', index=False)


