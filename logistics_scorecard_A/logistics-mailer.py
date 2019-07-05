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

TRIGGER_TO_CREATE = "%m"
TO_CREATE_SCORECARD = datetime.datetime.now() # 1-30

DAY_TO_SEND_TO_LOGISTICS = '' #

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
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
        print(datetime.datetime.now().strftime("%Y-%m-%d"))
        accounts = Account.objects.all()
        for i in accounts:
            print(f'CHECKING (ACTIVE) {str(i.user).upper()} — {i.service} @ {(datetime.datetime.now()).strftime("%Y-%m-%d %I:%M:%S %p")}')
            if i.is_active == True:
                ## CREATE SCORECARD
                al_scorecards = AppraiserList.objects.filter(account=i.pk).values_list('scorecard',flat=True)
                sc_dates = [x.strftime(TRIGGER_TO_CREATE) for x in list(Scorecard.objects.filter(id__in=al_scorecards).values_list('date_released',flat=True))] # QUERY DATES

                ## CREATE SCORECARD
                if TO_CREATE_SCORECARD.strftime(TRIGGER_TO_CREATE) not in sc_dates: # FILTER DAY
                    print(f'CREATING SCORECARD @ {(datetime.datetime.now()).strftime("%Y-%m-%d %I:%M:%S %p")}')
                    c = len(i.scorecard.all()) + 1
                    s = Scorecard.objects.create(cid=f'{str(i.user).upper()}SCORECARD{c}',
                                                 service=i.service,
                                                 account_manager=i.manager,
                                                 date_released=timezone.now(),
                                                )
                    s.category_list.set(i.template.category.all())
                    s.save()
                    ## UPDATE APPRAISER'S LIST
                    al = AppraiserList.objects.create(account=i,
                    scorecard=s,
                    )
                    al.save()

                ## SEND SCORECARDS
                for sc in AppraiserList.objects.filter(account=i.pk):
                    if sc.is_sent_sc == False:
                        print(f'SENDING TO:\t{i.user.email} @ {(datetime.datetime.now()).strftime("%Y-%m-%d %I:%M:%S %p")}')
                        msg = MIMEMultipart('alternative')
                        msg['To'] = i.user.email
                        msg['From'] = 'tester@artesyn.com'
                        msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"


                        EMAIL_BODY = """<h1>{{title}}</h1>
                                        <p>
                                        Hi {{user}}, it's time to score your monthly scorecards:&nbsp;
                                        <a title="ARTESYN SCORECARD" href="{{url}}">CLICK HERE</a>
                                        </p>
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
                            )
                        ,"html" )

                        msg.attach(msg_text)
                        msg.attach(msg_html)

                        ## FOR FEEDBACK SENDER
                        # with open('email.html', 'r', encoding='utf-8') as t:
                        #     template = t.read()
                        # with open("test.html","w",encoding='utf-8') as test:
                        #     test.write(
                        #     Environment().from_string(template).render(
                        #     title='ARTESYN LOGISTIC SCORECARD',
                        #     scorecard=sc.scorecard,
                        #     ratings=sc.scorecard.rating.all(),
                        #     )
                        #     )
                        #     test.close()

                        mailserver.sendmail('email', str(i.user.email), msg.as_string())

                        sc.is_sent_sc = True
                        sc.save()
                        print(f'{sc.scorecard} is SENT to {i.user.email}')


        sleep(2)

    mailserver.quit()

if __name__ == "__main__":
    main()