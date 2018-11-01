import numpy as np
import os

os.chdir('/home/daily_reports/Bond Yields/')

def render(yields, DGS10, T10Y2Y, T10YIE, moving_averages):
    print('RENDERING...')
    breakeven = float(T10YIE['T10YIE'].iloc[-1])
    spread = float(T10Y2Y['T10Y2Y'].iloc[-1])
    DGS10['DATE'] = DGS10['DATE'].apply(lambda x: x.strftime('%m/%d/%y'))
    yields.columns = ('Date', '1M', '2M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y')
    yields['Date'] = yields['Date'].apply(lambda x: x.strftime('%m/%d/%y'))
    moving_averages = ["{:.2f}".format(x) for x in moving_averages]
    with open('template.html', 'r+') as fh:
        html = fh.read()
    html = html.format(dataframe=yields.tail(10).to_html(index=False, border=0, table_id="yields", float_format=lambda x: '%.2f' % x), moving_averages=moving_averages, breakeven=breakeven, spread=spread)
    with open('index.html', 'w') as fh:
        fh.write(html)
