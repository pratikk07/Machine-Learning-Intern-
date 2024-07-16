import requests
import xlwt
from xlwt import Workbook
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from datetime import datetime
from email.utils import COMMASPACE, formatdate
import getpass

BASE_URL = "https://remoteok.com/api"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US en;q=0.5',
}

def get_job_postings():
    res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
    return res.json()

def truncate_string(value, max_length=32767):
    if isinstance(value, str) and len(value) > max_length:
        print(f"Truncating string: {value[:50]}... to {max_length} characters")
        return value[:max_length]
    return value

def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('jobs')
    headers = list(data[0].keys())
    
    for i in range(0, len(headers)):
        job_sheet.write(0, i, headers[i])
    
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(0, len(values)):
            job_sheet.write(i + 1, x, truncate_string(values[x]))
    
    wb.save('remote_jobs.xls')

def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    try:
        # Use Outlook SMTP server
        smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtp.starttls()
        
        # Prompt for the password securely
        password = getpass.getpass("Enter your Outlook email password: ")
        smtp.login(send_from, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        print("[*] Email sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print(f"[!] SMTP Authentication Error: {e.smtp_code} - {e.smtp_error.decode()}")
    except Exception as e:
        print(f"[!] An error occurred: {e}")
    finally:
        smtp.close()
        print("[*] SMTP connection closed")

if __name__ == "__main__":
    json = get_job_postings()[1:]
    output_jobs_to_xls(json)
    send_email('kolhepratik7057@outlook.com', ['pratikk6094@gmail.com'],
               'Jobs Posting', 'Please, find attached a list of job posting to this email',
               files=['remote_jobs.xls'])
