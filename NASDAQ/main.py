#! /usr/bin/env python3

import data, plot, technicals, render, distribute
import time
import pandas as pd
import os

os.chdir('/home/daily_reports/NASDAQ/')

start = time.time()

df = data.NASDAQCOM()
gainers, losers = data.movers()
stats = data.daily_stats()
faang = data.faang()
df_MA = technicals.moving_averages(df)
df_BB = technicals.bollinger_bands(df)
technicals = technicals.technicals(df)
fig1 = plot.NASDAQ(df)
render.render(df, df_BB, df_MA, stats, technicals, gainers, losers, faang)
distribute.to_pdf('index.html')
#distribute.send('DailyNASDAQReport.pdf')

print(time.time() - start)
