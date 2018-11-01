import os

os.chdir('/home/daily_reports/SP500/')

def render(df, df_bb, active, gainers, losers, details, ratios, performance):
    print("RENDERING...")
    df['% Chg'] = df['SP500'].pct_change() * 100
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%m/%d/%y'))
    SP500 = df.tail(10).round(2)
    SP500_html = SP500.to_html(index=False, border=0, table_id="SP500", float_format=lambda x: '%.2f' % x,
                               formatters={'% Chg': '{0:.2f}%'.format, 'SP500': '{0:,.2f}'.format})
    BB_html = df_bb.tail(1).drop(['Date'], axis=1).to_html(index=False, border=0, table_id="BB", float_format=lambda x: '{0:,.2f}'.format(x))
    active_html = active.to_html(index=False, classes="movers", border=0, table_id="active")
    gainers_html = gainers.to_html(index=False, classes="movers", border=0, table_id="gainers")
    losers_html = losers.to_html(index=False, classes="movers", border=0, table_id="losers")
    with open('/home/daily_reports/SP500/template.html', 'r') as fh:
        html = fh.read()

    html = html.format(SP500=SP500_html, BB=BB_html, active=active_html, gainers=gainers_html, losers=losers_html, range=details['52 week range'],
                       volume=details["Today's volume"], average_volume=details['Average daily volume (3 months)'], ratios=ratios, performance=performance)

    with open('/home/daily_reports/SP500/index.html', 'w') as fh:
        fh.write(html)
