import datetime
import requests
from time import sleep
import sys
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics_scorecard_A.settings")
django.setup()
# From now onwards start your script..
from survey_app.models import Scorecard
from survey_app.models import Account_manager

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()


msg['From'] = "from@email.com"
msg['To'] = "to@email.com"
msg['Subject'] = "LOGISTICS MONTHLY SCORECARD"

message = "MenRTrashMenRTrashMenRTrashMenRTrashMenRTrash"

# add in the message body
msg.attach(MIMEText(message, 'plain'))

mailserver = smtplib.SMTP('smtp.office365.com',587)
mailserver.ehlo()
mailserver.starttls()
mailserver.login(msg['From'], 'password')

while True:
    mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
    print("sent")
    sleep(5)

server.quit()

# for x in Account_manager.objects.all():
#    print (datetime.datetime.now().second)
#    time.sleep(1)
#    data = {'email':str(x.email), 'subject':'Logistic Scorecard', 'body':'http://localhost:8000/login/'}
#    # if datetime.datetime.now().second == 30:
#    #     requests.post('https://prod-23.southeastasia.logic.azure.com:443/workflows/3e1c9c57e9714d59b2a735a4fb4493a3/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ZJJl-dVZLdRhlV5kDALwT98fkSwEcPWPqOr6GWjp_og',
#    #                 json=data)
#    requests.post('https://prod-23.southeastasia.logic.azure.com:443/workflows/3e1c9c57e9714d59b2a735a4fb4493a3/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ZJJl-dVZLdRhlV5kDALwT98fkSwEcPWPqOr6GWjp_og', json=data)
