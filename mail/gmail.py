# Import smtplib for the actual sending function
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import json
import logging
import os.path as op

logging.basicConfig(level=logging.INFO, format='%(message)s')

class Gmail():
    def __init__(self):
        self.logger = logging.getLogger(__name__)                
        self.sent_from = 'PASS-42'  
        account = json.load(open('/usr/local/info/gmail.json', 'r'))
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.login(account['name'], account['password'])
        self.logger.info('LOGIN SUCCEED.')        


    def sendmail(self, mailto, body, subject='SUBJECT OMITTED', files=[]):
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain','utf-8'))
        msg['subject'] = Header(subject, 'utf-8')
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1,utf-8"

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

        try:
            self.server.sendmail(self.sent_from, mailto, msg.as_string())
            self.server.close()            
        except Exception as e:
            self.server.close()                        
            raise e
        self.logger.info('MAIL SENT!')



if __name__ == '__main__':
    gm = Gmail()
    gm.sendmail(['ssrzz@pm.me'], 'Are you okay?', subject='Essential')
