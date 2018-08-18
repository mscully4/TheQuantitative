#! /usr/bin/env python3

import refresh_nominal, refresh_real, moving_averages, plot, render, distribute
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

print("Executing File ./Bond Yields/main.py")
os.chdir('/home/daily_reports/Bond Yields/')

start = time.time()

refresh_nominal.refresh()
refresh_real.refresh()
data = 'data.csv'
df = pd.read_csv(data, parse_dates=['Date'], dtype=float)
df_MA = moving_averages.moving_averages(df)
df_real = pd.read_csv('dataR.csv', parse_dates=['DATE'], dtype=float)
fig1 = plot.yield_curve(df)
fig2 = plot.yield_spread(df)
fig3 = plot.moving_averages(df, df_MA)
fig4 = plot.exponential_moving_averages(df, df_MA)
fig5 = plot.breakeven_rate(df, df_real)
moving_averages = tuple([float(df.loc[len(df) - 1, x]) for x in df.columns[12:18]])
render.render(df, df_real, df_MA, 'template.html', 'index.html')
distribute.to_pdf('index.html')
#distribute.send('DailyTreasuryYieldReport.pdf')
    
print(time.time() - start)
