def render(df, df_bb, df_ma, stats, technicals, gainers, losers, faang):
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%m/%d/%y'))
    NASDAQ = df.tail(10).round(2)
    NASDAQ.columns = ['Date', 'NASDAQ', '% Chg']
    NASDAQ = NASDAQ.to_html(index=False, border=0, table_id="NASDAQ", float_format=lambda x: '%.2f' % x,
                               formatters={'% Chg': '{0:.2f}%'.format, 'SP500': '{0:,.2f}'.format})
    MA_html = df_ma.tail(1).drop(['Date'], axis=1).to_html(index=False, border=0, table_id="MA", float_format=lambda x: '%.2f' % x)
    BB_html = df_bb.tail(1).drop(['Date'], axis=1).to_html(index=False, border=0, table_id="BB", float_format=lambda x: '%.2f' % x)
    gainers_html = gainers.to_html(index=False, classes="movers", border=0, table_id="gainers")
    losers_html = losers.to_html(index=False, classes="movers", border=0, table_id="losers")
    with open('template.html', 'r') as fh:
        html = fh.read()

    html = html.format(NASDAQ=NASDAQ, BB=BB_html, MA=MA_html, stats=stats, technicals=technicals, gainers=gainers_html,
                       losers=losers_html, faang=faang)

    with open('index.html', 'w') as fh:
        fh.write(html)