import imaplib, email
import clipboard
from bs4 import BeautifulSoup
import re
import os
import django
import getpass
user = 'ButchPaoloMadahan@artesyn.com'
password = getpass.getpass()
url = 'outlook.office365.com'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics_scorecard_A.settings")
django.setup()
from survey_app.models import *
from users.models import *

mail = imaplib.IMAP4_SSL(url)
mail.login(user,password)
mail.select('INBOX')

result, data = mail.search(None, "ALL")

ids = data[0]
email_ids = ids.split() 
print(email_ids)
scorecards = Scorecard.objects.filter(is_locked=False)
print(scorecards)
last = email_ids[-1]

for specific_id in email_ids:
    result, data = mail.fetch(specific_id, "(RFC822)")
    x = data[0][1]
    msg = email.message_from_string(x.decode("utf-8"))
    strtext=""
    print(msg['from'])
    for scorecard in scorecards:
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
                                category = scorecard.category_list.get(category_number = category_num)
                                question = category.questions.get(question_number = question_num)
                                scorecard.feedback.get_or_create(question=Question(question.id), feedback=feedback)
                                # print(scorecard_feedback)
                                
                                # rating.feedback = feedback
                                # rating.save()
                                # print(rating.feedback)
                                #print(rating.question.question_string)
                                #print("original id: " + each1["id"])
                                #print(new_id[0][3:] + str(each1.getText()))
                        else:
                            print(str(each1.gettext()))    
