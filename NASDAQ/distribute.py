import pdfkit
from os.path import basename
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

def to_pdf(filename):
    options = {
    'page-size': 'Letter',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'disable-smart-shrinking': '',
    'quiet': '',
    }

    pdfkit.from_file(filename, '/home/daily_reports/NASDAQ/DailyNASDAQReport.pdf', options=options)
