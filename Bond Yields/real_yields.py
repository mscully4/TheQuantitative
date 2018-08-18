import pandas as pd
import requests
import bs4
import time
import datetime
import os

os.chdir('/home/daily_reports/Bond Yields/')

url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyieldAll"
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
    if q % 6 == 0:
        z += 1
    try:
        df.loc[z, columns[q % 6]] = float(entry.text)
    except ValueError:
        if entry.text == "\n\t\t\tN/A\n\t\t" or entry.text =="N/A":
            df.loc[z, columns[q % 6]] = None
        else:
            df.loc[z, columns[q % 6]] = pd.Timestamp(entry.text)

df.to_csv('/home/daily_reports/Bond Yields/dataR.csv', index=False)
