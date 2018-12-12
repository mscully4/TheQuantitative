import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from os.path import basename
import os
import os.path
import configparser as cp

os.chdir('/home/daily_reports/PDFs/')

config = cp.ConfigParser()
config.read("config.ini")

def send(filename):
    print('SENDING...')
    fromaddr = config.get('Email', 'address')
    toaddrs = 'mscully4@nd.edu'
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = "The Quantitative -- Daily Financial Report"
    with open(filename, "rb") as fh:
                msg.attach(MIMEApplication(
                    fh.read(),
                    Content_Disposition='attachment; filename="%s"' % basename(filename),
                    Name=basename(filename)
                ))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, config.get('Email', 'password'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddrs, text)
    print('...')
    print('SENT')
    server.quit()


