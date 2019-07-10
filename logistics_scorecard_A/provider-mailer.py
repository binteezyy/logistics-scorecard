## DEFAULT LIBS
import smtplib, sys, os
from getpass import getpass

## TIME
from django.utils                               import timezone
from time                                       import sleep
import datetime

## EMAIL TEMPLATING MODULES
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment # FOR HTML ATTACHMENT
from bs4 import BeautifulSoup

### DJANGO
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics_scorecard_A.settings")
django.setup()

## DJANGO MODELS
from survey_app.models import *
from users.models import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def update():
    schedule_trigger = Trigger.objects.get(pk=1)
    PROVIDER_FEEDBACK_TRIGGER = f'{schedule_trigger.send_to_providers_trigger}'
    PROVIDER_FEEDBACK_TIME = f'{schedule_trigger.send_to_providers_value}'

    return {'PROVIDER_FEEDBACK_TRIGGER': PROVIDER_FEEDBACK_TRIGGER,
            'PROVIDER_FEEDBACK_TIME': PROVIDER_FEEDBACK_TIME,
            }

def main():
    schedule_trigger = Trigger.objects.get(pk=1)
    smpt_set = schedule_trigger.use_fake_smtp
    msg = MIMEMultipart('alternative')
    mailserver = smtplib.SMTP('')

    print("(1)365.OUTLOOK\t(2)fakeSMTP")
    if smpt_set == False:
        print("365.OUTLOOK")

        msg['From'] = input("EMAIL:")
        msg['PWD'] = getpass()

        mailserver = smtplib.SMTP('smtp.office365.com',587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(msg['From'],msg['PWD'])

    elif smpt_set == True:
        print("fakeSMTP")
        msg['From'] = "SERVICE ACCOUNT"
        mailserver = smtplib.SMTP('localhost',25)
        mailserver.ehlo()
    else:
        print("INVALID smpt_set")

    clear()

    while True:
        SETTINGS = update()
        print(f'PROVIDER MAILER || {datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')
        accounts = Account.objects.all()
        if (datetime.datetime.now().strftime(SETTINGS['PROVIDER_FEEDBACK_TRIGGER']) == SETTINGS['PROVIDER_FEEDBACK_TIME']): #
            for i in accounts:
                if i.is_active == True:
                    print(f'CHECKING (ACTIVE) {str(i.user).upper()} — {i.service} @ {(datetime.datetime.now()).strftime("%Y-%m-%d %I:%M:%S %p")}')

                    for sc in AppraiserList.objects.filter(account=i.pk):
                        if (sc.feedback_sent == None and sc.scorecard.is_applicable == True
                           and sc.scorecard.is_rated == True and sc.scorecard.is_approved == True):
                            msg['Subject'] = "DAILY REMINDER: LOGISTICS MONTHLY SCORECARD"
                            msg['To'] = sc.scorecard.account_manager.email

                            print(f'SENDING FEEDBACK TO {sc.scorecard.account_manager.email}')

                            ## BOOTSTRAP
                            with open('email.html', 'r', encoding='utf-8') as t:
                                template = t.read()

                            ## EDITED PREVIEW
                            # with open('email_send.html', 'w+', encoding='utf-8') as test:
                            #     test.write(
                            #         Environment().from_string(template).render(
                            #         title='ARTESYN LOGISTIC SCORECARD',
                            #         scorecard=sc.scorecard,
                            #         ratings=sc.scorecard.rating.all(),
                            #         )
                            # )
                            # test.close()

                            with open('email_send.html', 'r', encoding='utf-8') as temp:
                                soup = str(BeautifulSoup(temp))
                                msg_html = MIMEText(
                                Environment().from_string(soup).render(
                                    title='ARTESYN LOGISTIC SCORECARD: FEEDBACK FORM',
                                    scorecard=sc.scorecard,
                                    ratings=sc.scorecard.rating.all(),
                                    )
                                ,"html" )

                            EMAIL_BODY = ""
                            msg_text = MIMEText(EMAIL_BODY,'plain')
                            msg.attach(msg_html)
                            try:
                                mailserver.sendmail(str(msg['From']), msg['To'], msg.as_string())
                                sc.feedback_sent = timezone.now()
                                sc.save()
                            except:
                                print("ERROR")
        sleep(1)

    mailserver.quit()

if __name__ == "__main__":
    main()
