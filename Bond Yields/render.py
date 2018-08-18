import numpy as np
import os

os.chdir('/home/daily_reports/Bond Yields/')

def render(df, df_real, df_MA, template, index):
    print('RENDERING...')
    breakeven = np.round(float(df.loc[(len(df) - 1), '10 yr']) - float(df_real.loc[(len(df_real) - 1), '10 YR']), 2)
    spread = np.round(float(df.loc[(len(df) - 1), '10 yr']) - float(df.loc[(len(df) - 1), '2 yr']), 2)
    moving_averages = np.round(tuple(df_MA.loc[len(df_MA) - 1])[1:], 2)
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%m/%d/%y'))
    df.columns = ('Date', '1M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y')
    with open('template.html', 'r+') as fh:
        html = fh.read()
    html = html.format(dataframe=df.tail(10).to_html(index=False, border=0), MA50=moving_averages[0], \
                       MA100=moving_averages[1], MA200=moving_averages[2], EWMA50=moving_averages[3], \
                       EWMA100=moving_averages[4], EWMA200=moving_averages[5], Breakeven=breakeven, Spread=spread)
    with open('index.html', 'w') as fh:
        fh.write(html)
