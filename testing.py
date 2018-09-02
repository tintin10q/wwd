import smtplib

sender = 'tintin10q@hotmail.com'
receivers = ['tintin10q@hotmail.com']

message = """From: From Person <tintin10q@hotmail.com>
To: To Person <tintin10q@hotmail.com>
Subject: Email test

This is a test e-mail message.

Groeten,
Quinten
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except SMTPException:
   print("Error: unable to send email")