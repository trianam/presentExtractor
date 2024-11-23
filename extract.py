#! /usr/bin/env python

import pandas as pd
import json
import random
import smtplib
from email.mime.text import MIMEText

debugRep = 100000
# debug = False
debug = True
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

stats = dict()
for name1 in users['mails'].keys():
    stats[name1] = dict()
    for name2 in users['mails'].keys():
        stats[name1][name2] = 0

for rep in range(debugRep if debug else 1):
    result = dict()
    extracted = set()

    while len(result) == 0:
        try:
            shuffledNames = list(users['mails'].keys())
            random.shuffle(shuffledNames)
            for name in shuffledNames:
                possibles = set([ k for k in users['possibilities'][name] if users['possibilities'][name][k] == True ])
                result[name] = random.sample(list(possibles - extracted), 1)[0]
                extracted.add(result[name])
        except:
            result = dict()
            extracted = set()

    for name in result.keys():
        if rep == 0:
            print("Send to {} ({})".format(name, users['mails'][name]))
            sendMessage(name, result[name], debug)

        stats[name][result[name]] += 1


if debug:
    print(f"Frequencies over {debugRep}:")
    for k1 in sorted(stats.keys()):
        print(f"{k1} -> {[f'{k2}: {stats[k1][k2]}' for k2 in sorted(stats[k1].keys())]}")

    print(f"Probabilities over {debugRep}:")
    for k1 in sorted(stats.keys()):
        print(f"{k1} -> {[f'{k2}: {stats[k1][k2]/debugRep*100:.1f}%' for k2 in sorted(stats[k1].keys())]}")

print("\nExtraction process completed")

