#! /usr/bin/env python3

import data, plot, technicals, render, distribute
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

os.chdir('/home/daily_reports/SP500/')
print(os.getcwd())

start = time.time()

df = data.SP500()
df_bb = technicals.bollinger_bands(df)
details = data.quote_details()
ratios = data.ratios()
performance = data.performance(df)
active, gainers, losers = data.big_movers()
fig1 = plot.SP500(df)
render.render(df, df_bb, active, gainers, losers, details, ratios, performance)
distribute.to_pdf('index.html', 'DailySP500Report.pdf')

print("DURATION: {}".format(time.time() - start))
