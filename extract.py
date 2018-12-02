#! /usr/bin/env python

import pandas as pd
import json
import random
import smtplib
from email.mime.text import MIMEText

data = json.load(open("data.json", 'rt'))
users = json.load(open("users.json", 'rt'))

def sendMessage(dest, objective, debug=False):
    if debug:
        print("\t {} -> {}".format(dest, objective))
    else:
        msg = MIMEText(data['msgBase'] + objective)

        msg['Subject'] = data['subject']
        msg['From'] = data['from']
        msg['To'] = users['mails'][dest]

        smtpObj = smtplib.SMTP_SSL(data['smtp'], data['port'])
        smtpObj.login(data['user'], data['password'])
        smtpObj.send_message(msg)
        smtpObj.quit()


df = pd.DataFrame(users['possibilities'])
print("Possibilities:")
print(df.to_string(na_rep='-'))
print("")


result = dict()
extracted = set()

while len(result) == 0:
    try:
        for name in users['mails'].keys():
            possibles = set([ k for k in users['possibilities'][name] if users['possibilities'][name][k] == True ])
            result[name] = random.sample(possibles - extracted, 1)[0]
            extracted.add(result[name])
    except:
        result = dict()
        extracted = set()

for name in result.keys():
    print("Send to {} ({})".format(name, users['mails'][name]))
    sendMessage(name, result[name])

print("\nExtraction process completed")

