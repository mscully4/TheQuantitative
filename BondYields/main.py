#! /usr/bin/env python3

import moving_averages, plot, render, distribute, data
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

print("Executing File ./BondYields/main.py")
os.chdir('/home/daily_reports/BondYields/')

start = time.time()

yields = data.yields()
DGS10 = data.DGS10()
T10YIE = data.T10YIE()
T10Y2Y = data.T10Y2Y()
year_ago = data.year_ago(yields)
#refresh_nominal.refresh()
#refresh_real.refresh()
#data = 'data.csv'
#df = pd.read_csv(data, parse_dates=['Date'], dtype=float)
df_MA = moving_averages.moving_averages(DGS10)
#df_real = pd.read_csv('dataR.csv', parse_dates=['DATE'], dtype=float)
fig1 = plot.yield_curve(yields, year_ago)
fig2 = plot.yield_spread(T10Y2Y)
fig3 = plot.moving_averages(df_MA)
#fig4 = plot.exponential_moving_averages(df, df_MA)
fig5 = plot.breakeven_rate(T10YIE)
moving_averages = list(df_MA.iloc[-1])[2:]
render.render(yields, DGS10, T10Y2Y, T10YIE, moving_averages)
distribute.to_pdf('index.html', 'DailyTreasuryYieldReport.pdf')
    
print(time.time() - start)
