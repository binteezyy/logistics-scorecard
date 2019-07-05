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

### DJANGO
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics_scorecard_A.settings")
django.setup()

## DJANGO MODELS
from survey_app.models import *
from users.models import *

TIME_TRIGGER = '%#S' if os.name == 'nt' else '%-S'
TIME_TO_UPDATE_LOG = '0' # DEPENDS ON TIME TRIGGER
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    msg = MIMEMultipart('alternative')
    mailserver = smtplib.SMTP('')

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


    clear()
    while True:
        print( datetime.datetime.now().strftime(TIME_TRIGGER))
        accounts = Account.objects.all()
        for i in accounts:
            if i.is_active == True:
                if datetime.datetime.now().strftime(TIME_TRIGGER) == TIME_TO_UPDATE_LOG:
                    print(f'CHECKING SCORECARD STATUS (ACTIVE) {str(i.user).upper()} — {i.service} @ {(datetime.datetime.now()).strftime("%Y-%m-%d %I:%M:%S %p")}')
                    for sc in AppraiserList.objects.filter(account=i.pk):
                        if ((sc.is_notified == None or datetime.datetime.now().day == sc.is_notified.day+1)
                             and sc.is_sent_sc == True and sc.scorecard.is_applicable == False):
                            print(f'SENDING TO:\t{i.user.email} @ {(datetime.datetime.now()).strftime("%Y-%m-%d %I:%M:%S %p")}')
                            msg = MIMEMultipart('alternative')
                            msg['To'] = i.user.email
                            msg['From'] = 'tester@artesyn.com'
                            msg['Subject'] = "DAILY REMINDER: LOGISTICS MONTHLY SCORECARD"

                            EMAIL_BODY = """<h1>{{title}}</h1>
                                            <p>
                                            Hi {{user}}, you haven't answered your scorecard yet:&nbsp;
                                            <a title="ARTESYN SCORECARD" href="{{url}}">CLICK HERE TO ANSWER</a>
                                            </p>
                                            <p> Kindly answer the monthly scorecard before {{enddate}} </p>
                                            """

                            EMAIL_BODY_LANDING_URL = 'http://localhost:8000/login'
                            ## PLAIN TEXT BODY
                            msg_text = MIMEText("TEXT",'plain')

                            ## HTML BODY
                            ## EDITOR https://html-online.com/editor/
                            msg_html = MIMEText(
                            Environment().from_string(EMAIL_BODY).render(
                                title='ARTESYN LOGISTIC SCORECARD',
                                user= i.user,
                                url= EMAIL_BODY_LANDING_URL,
                                enddate = sc.scorecard.date_released.strftime('%B 15,%Y')
                                )
                            ,"html" )

                            msg.attach(msg_text)
                            msg.attach(msg_html)

                            mailserver.sendmail('email', str(i.user.email), msg.as_string())
                            sc.is_notified = timezone.now();
                            sc.save()
                            print(f"{i.user}'s NOTIF FLAG HAS BEEN RESET TO {('True' if sc.is_notified != None else 'False')}")
                if datetime.datetime.now().strftime(TIME_TRIGGER) == '0':
                    print(f'RESETTING SCORECARDS {datetime.datetime.now()}')
                    for sc in AppraiserList.objects.filter(account=i.pk):
                        if sc.is_notified != None and sc.is_sent_sc == True and sc.scorecard.is_applicable == False:
                            sc.is_notified = None;
                            sc.save()
                            print(f"{i.user}'s NOTIF FLAG HAS BEEN RESET TO {('True' if sc.is_notified != None else 'False')}")
        sleep(1)
    mailserver.quit()

if __name__ == "__main__":
    main()