#! /usr/bin/env python3

import refresh, plot, bollinger_bands, render, distribute
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

print("EXECUTING FX\main.py")
start = time.time()

os.chdir('/home/daily_reports/FX/')

refresh.refresh()
df = pd.read_csv('FX.csv', parse_dates=['Date'], dtype=float)
fig1 = plot.plot_developed_currencies(df)
fig2 = plot.plot_emerging_currencies(df)
fig3 = plot.plot_trade_weighted_dollar()
bands = bollinger_bands.generate_bollinger_bands(df)
render.render(df, bands, 'template.html', 'index.html')
distribute.to_pdf('index.html', 'DailyForeignExchangeReport.pdf')
#distribute.send('DailyForeignExchangeReport.pdf')


print(time.time() - start)

