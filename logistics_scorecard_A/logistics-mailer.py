import datetime
import requests
import smtplib
from time import sleep
import sys, os
import datetime
from getpass import getpass

import base64

from pprint import pprint
from jinja2 import Environment        # Jinja2 templating

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics_scorecard_A.settings")
django.setup()

from survey_app.models import *
from users.models import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

msg = MIMEMultipart()
mailserver = smtplib.SMTP('')
with open('email.html', 'r', encoding='utf-8') as t:
    template = t.read()


print("(1)365.OUTLOOK\t(2)fakeSMTP")
selection=input("Please Select:")
if selection =='1':
    print("365.OUTLOOK")

    msg['From'] = input("EMAIL:")
    msg['PWD'] = getpass()

    mailserver = smtplib.SMTP('smtp.office365.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(msg['From'],msg['PWD'])

elif selection == '2':
    print("fakeSMTP")
    mailserver = smtplib.SMTP('localhost',25)
    mailserver.ehlo()



else:
    print("INVALID SELECTION")


while True:
    # PARSE ACCOUNTS
    accounts = Account.objects.all()

    for i in accounts:
        print(i.user, '——', i.service)
        ## CHECK EXISTING SCORECARD THIS MONTH
            ## INSERT CONDITION

        ## CREATE SCORECARD
        if i.is_active == True:
            for sc in AppraiserList.objects.filter(account=i.pk):
                if sc.is_sent_sc == False:

                    print("SENDING TO:\t",i.user.email,"\n")

                    msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"
                    msg = MIMEText(
                        Environment().from_string(template).render(
                            title='ARTESYN LOGISTIC SCORECARD',
                            scorecard=sc.scorecard,
                            ratings=sc.scorecard.rating.all(),
                        ), "html"
                    )
                    pprint(sc.scorecard.rating.all())
                    # SAMPLE OUTPUT
                    with open("test.html","w",encoding='utf-8') as test:
                        test.write(
                            Environment().from_string(template).render(
                                title='ARTESYN LOGISTIC SCORECARD',
                                scorecard=sc.scorecard,
                                ratings=sc.scorecard.rating.all(),
                            )
                        )
                        test.close()

                    mailserver.sendmail('email', str(i.user.email), msg.as_string())
                    sc.is_sent_sc = True
                    sc.save()

                    print(sc.scorecard,"\t",sc.is_sent_sc)
                    c = len(i.scorecard.all()) + 1
                    s = Scorecard.objects.create(cid="SCORECARD%d" % (c),
                                                date_released=datetime.datetime.now(),
                                                account_manager=i.manager,
                                                )
                    s.save()
                    al = AppraiserList.objects.create(account=sc.account,
                                                is_sent_sc=True,
                                                scorecard=s,
                                                )
                    al.save()


    sleep(2)

mailserver.quit()

# if __name__ == "__main__":
#     main()
