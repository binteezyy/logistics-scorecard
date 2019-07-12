import imaplib, email
from bs4 import BeautifulSoup
import re
import os
import clipboard
from time import sleep
import smtplib
import django
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
user = 'ButchPaoloMadahan@artesyn.com'
password = getpass.getpass()
url = 'outlook.office365.com'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics_scorecard_A.settings")
django.setup()
from survey_app.models import *
from users.models import *
trigger = Trigger.objects.last()
mail = imaplib.IMAP4_SSL(url)
mail.login(user,password)
mail.select('INBOX')


while True:
    result, data = mail.search(None, "ALL")

    ids = data[0]
    email_ids = ids.split()
    print(email_ids[-1])
    scorecards = Scorecard.objects.filter(is_locked=False, is_rated=True, is_applicable=True)
    print(scorecards)
    # last = email_ids[-1]
    # if datetime.datetime.now().day > 15:
    if datetime.datetime.now().day > trigger.extract_feedbacks:
        for specific_id in email_ids:
            result, data = mail.fetch(specific_id, "(RFC822)")
            x = data[0][1]
            msg = email.message_from_string(x.decode("utf-8"))
            strtext=""
            print(msg['from'])
            for scorecard in scorecards:
                frm = msg['from']
                print(f'{scorecard.account_manager.email} — {frm}')
                if scorecard.account_manager.email in msg['from']:
                    print(str(scorecard.account_manager.email) + str(msg['from']))
                    try:
                        if msg.is_multipart():
                            for part in msg.walk():
                                print("Multipart")
                                payload = part.get_payload(decode=True)
                                if payload:
                                    strtext = payload.decode() #utf-8 is default
                                    # print(strtext)
                        else:
                            payload = msg.get_payload(decode=True)
                            print("Not multipart")
                            strtext = payload.decode()
                    except:
                        pass
                    # clipboard.copy(str(strtext))
                    # print("Copied!")
                    html = BeautifulSoup(str(strtext), 'html.parser')

                    tables = html.find_all('table', attrs={'name':'cattable'})
                    # clipboard.copy(str(tables))
                    cid =""
                    cid = html.find('td', attrs={'name':'scorecardcid'})
                    if cid:
                        cid = cid.getText()
                        cid = [item.strip() for item in cid if str(item)]
                        cid = ''.join(cid)
                        print(str("From db: ") + scorecard.cid)
                        print(str("From email: ") + str(cid))
                    if cid == scorecard.cid:
                        print("CID is validated!")
                        for table in tables:
                            p = table.find_all('td', attrs={'name':'feedback'})
                            for each1 in p:
                                if each1["id"] is not None:
                                    if ":" in each1["id"]:
                                        cut_id = each1["id"].split(":")
                                        new_id = cut_id[1].split("-")
                                        category_num = new_id[0][3:]
                                        question_num = new_id[1][1:]
                                        feedback = str(each1.getText())
                                        print(category_num + feedback)
                                        category = scorecard.category_list.get(category_number = category_num)
                                        question = category.questions.get(question_number = question_num)
                                        scorecard.feedback.get_or_create(question=Question(question.id), feedback=feedback)


                                else:
                                    print(str(each1.gettext()))
                        for i in User.objects.all():
                            try:
                                for u in Account.objects.get(user=i).scorecard.all():
                                        if u == scorecard:
                                            msg = MIMEMultipart()
                                            msg['From'] = "ButchPaoloMadahan@artesyn.com"
                                            msg['To'] = i.email
                                            msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"

                                            message = "Testing!"

                                            msg.attach(MIMEText(message, 'plain'))

                                            mailserver = smtplib.SMTP('smtp.office365.com',587)
                                            mailserver.ehlo()
                                            mailserver.starttls()
                                            mailserver.login(msg['From'], password)
                                            try:
                                                mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
                                                scorecard.is_locked = True
                                                scorecard.is_rated = False
                                                scorecard.is_approved = False
                                                scorecard.save()
                                            except:
                                                scorecard.is_locked = False
                                                scorecard.save()
                            except:
                                pass
    sleep(1)
