import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from os.path import basename
import os

os.chdir('/home/daily_reports/Bond Yields/')

def to_pdf(filename):
    options = {
    'page-size': 'Letter',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'quiet': '',
    }
    pdfkit.from_file(filename, 'DailyTreasuryYieldReport.pdf', options=options)

def send(filename):
    fromaddr = "michael.scully1997@gmail.com"
    toaddr = 'mscully4@nd.edu'
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Daily Treasury Yield Report"

    with open(filename, "rb") as fh:
                msg.attach(MIMEApplication(
                    fh.read(),
                    Content_Disposition='attachment; filename="%s"' % basename(filename),
                    Name=basename(filename)
                ))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "AFarewellToArms&*90")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print('...')
    print('SENT')
    server.quit()
