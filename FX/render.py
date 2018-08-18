import bollinger_bands
import pandas as pd
import os

os.chdir('/home/daily_reports/FX/')

def render(df, bands, template, index):
    print("RENDERING")
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%m/%d/%y'))
    table = df.tail(10).round(decimals=2).to_html(index=False, border=0, table_id="timeseries", float_format=lambda x: '%.2f' % x)
    technicals = bands.drop('30 Day STD', axis=1).to_html(index=False, table_id="bands", border=0, float_format=lambda x: '%.2f' % x)
    with open(template, 'r+') as fh:
        html = fh.read()
    html = html.format(dataframe=table, bands=technicals)
    with open(index, 'w') as fh:
        fh.write(html)
