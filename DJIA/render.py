import data, technicals
import pandas as pd
import os

os.chdir('/home/daily_reports/DJIA/')

def render(performance, df_MA, df_BB):
    df = data.DJIA()
    df = df[df.columns.tolist()[::-1]]
    df['% Change'] = df['DJIA'].pct_change() * 100
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%m/%d/%y'))
    dow = df.tail(10).round(2)
    frmt = lambda x: '{0:.2f}%'.format(float(x))
    dow_html = dow.to_html(index=False, border=0, table_id="DJIA", float_format=lambda x: '%.2f' % x, formatters={'% Change': '{0:.2f}%'.format, 'DJIA': '{0:,.2f}'.format})
    components = data.components()
    winners = components.head(8).to_html(index=False, border=0, classes="components", table_id="winners", formatters={'Weight': '{0:.2f}%'.format, 'Change': '{0:.2f}'.format, '% Change': '{0:.2f}%'.format}, justify="left")
    losers = components.tail(8).to_html(index=False, border=0, classes="components", table_id="losers", formatters={'Weight': '{0:.2f}%'.format, 'Change': '{0:.2f}'.format, '% Change': '{0:.2f}%'.format}, justify="left")
    moving_averages = ['{:.2f}'.format(x) for x in df_MA.iloc[-1][2:]]
    bollinger_bands = ['{:.2f}'.format(x) for x in df_BB.iloc[-1][1:]]
    df['Date'] = df['Date'].astype(pd.Timestamp)
    for x in range(len(df)):
        df.loc[x, 'Date'] = pd.Timestamp(df.loc[x, 'Date'])
    with open("template.html", "r") as fh:
        html = fh.read()
    html = html.format(DJIA=dow_html, performance=performance, winners=winners, losers=losers, MA=moving_averages, BB=bollinger_bands)
    with open("index.html", "w") as fh:
        fh.write(html)
