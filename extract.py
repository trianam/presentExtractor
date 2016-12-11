#! /usr/bin/env python

import random
import smtplib
from email.mime.text import MIMEText

def sendMessage(dest, subject, message):
    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = 'xxx@xxx.xxx'
    msg['To'] = dest

    smtpObj = smtplib.SMTP_SSL('smtp.xxx.xxx', 465)
    smtpObj.login('xxx@xxx.xxx', 'xxx')
    smtpObj.send_message(msg)
    smtpObj.quit()



mails = {
    'Stefano': 'xxx@xxx.xxx',
    'Federica': 'xxx@xxx.xxx', 
    'Chiara': 'xxx@xxx.xxx',
    'Alberto': 'xxx@xxx.xxx',
    'Sara': 'xxx@xxx.xxx',
    'Lorenzo': 'xxx@xxx.xxx'}

possibles = {
    'Stefano': {'Chiara', 'Alberto', 'Sara', 'Lorenzo'},
    'Federica': {'Chiara', 'Alberto', 'Sara', 'Lorenzo'},
    'Chiara': {'Stefano', 'Federica', 'Sara', 'Lorenzo'},
    'Alberto': {'Stefano', 'Federica', 'Sara', 'Lorenzo'},
    'Sara': {'Stefano', 'Federica', 'Chiara', 'Alberto'},
    'Lorenzo': {'Stefano', 'Federica', 'Chiara', 'Alberto'}}

result = dict()
extracted = set()

while len(result) == 0:
    try:
        for name in mails.keys():
            result[name] = random.sample(possibles[name] - extracted, 1)[0]
            extracted.add(result[name])
    except:
        result = dict()
        extracted = set()

for name in mails.keys():
    sendMessage(mails[name], 'Regali per il compleanno di Zoroastro', "Complimenti! Sei stata/o scelta/o per fare il regalo a:\n"+result[name])

print("Extraction process completed")

