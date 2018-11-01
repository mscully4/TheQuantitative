from PyPDF2 import PdfFileMerger, PdfFileReader

def merge():
    print('MERGING...')
    BASE_DIR = '/home/daily_reports/'
    pdfs = ('SP500/DailySP500Report.pdf','NASDAQ/DailyNASDAQReport.pdf','DJIA/DailyDJIAReport.pdf','Bond Yields/DailyTreasuryYieldReport.pdf','FX/DailyForeignExchangeReport.pdf')

    merger = PdfFileMerger()

    for pdf in pdfs:
        print(BASE_DIR + pdf)
        merger.append(PdfFileReader(open(BASE_DIR + pdf, 'rb')), import_bookmarks=False)

    merger.write('/home/daily_reports/PDFs/The Quantitative -- Daily Financial Report.pdf')