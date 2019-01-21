Send [Gmail](https://mail.google.com) with Python3 `smtblib`. 

* use `MIMEText(body, 'plain', 'utf-8')` to encode non-English characters
* use `MIMEMultipart` to add attachments 
* use `msg['subject'] = subject` to set up subject 
* do not forget the `msg.as_string()` method before sending mail.

See the code: [`gmail.py`](https://raw.githubusercontent.com/ssrzz/webscraping/master/mail/gmail.py) for more detail. 