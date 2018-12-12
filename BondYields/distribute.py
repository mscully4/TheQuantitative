import pdfkit
from os.path import basename
#from PyPDF2 import PdfFileWriter, PdfFileReader
import os

def to_pdf(filename, output):
    options = {
    'page-size': 'Letter',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
 #   'disable-smart-shrinking': '',
    'quiet': '',
    }

    pdfkit.from_file(filename, output, options=options)
##    infile = PdfFileReader('DJIA Daily Report.pdf', 'rb')
##    output = PdfFileWriter()
##    output.addPage(infile.getPage(0))
##    with open('DJIA Daily Report.pdf', 'wb') as fh:
##        output.write(fh)
