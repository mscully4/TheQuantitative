#! /usr/bin/env python3

import data, technicals, plot, render, distribute
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

os.chdir('/home/daily_reports/DJIA/')

start = time.time()

df = data.DJIA()
components = data.components()
performance = data.performance(df)
fig1 = plot.DowJonesIndustrialAverageWBollingerBands(df)
df_MA = technicals.moving_averages(df)
df_BB = technicals.bollinger_bands(df)
render.render(performance, df_MA, df_BB)
distribute.to_pdf('/home/daily_reports/DJIA/index.html')
#distribute.send('/home/daily_reports/DJIA/DJIA Daily Report.pdf')

print(time.time() - start)
