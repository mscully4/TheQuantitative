import pandas as pd
import forex_python.converter as fx
import datetime as dt
import os

os.chdir('/home/daily_reports/FX')
def refresh():
    print("GATHERING DATA...")
    df = pd.read_csv('FX.csv', parse_dates=['Date'], dtype=float)
    now = pd.Timestamp(dt.date.today())
    date = now
    while True:
        if date in tuple(df['Date']):
            start = date
            break
        date = date - dt.timedelta(1)

    c = fx.CurrencyRates()
    currencies = ('EUR','GBP','JPY','CNY','INR','RUB','CHF','CAD','MXN')
    length = len(df)
    
    for x in range((now - start).days):
        try:
            rates = c.get_rates('USD', date + dt.timedelta(x + 1))
            df.loc[length + x, 'Date'] = date + dt.timedelta(x + 1)
            df.loc[length + x, '(USD)'] = 1
            for i in range(len(currencies)):
                df.loc[length + x, '({})'.format(currencies[i])] = rates[currencies[i]]
        except fx.RatesNotAvailableError:
            pass
    df = df.drop_duplicates(subset=['(EUR)', '(GBP)', '(JPY)', '(CNY)', '(INR)','(RUB)','(CHF)','(CAD)','(MXN)'], keep='first')
    print(df.tail(10))
    df.to_csv('FX.csv', index=None, float_format='%g')
    



