import datetime
import requests
import time 

data = {'email':'butchpaolom@gmail.com', 'subject':'TESTING', 'body':'tester'}

while(True):
    print (datetime.datetime.now().second)
    time.sleep(1)
    if datetime.datetime.now().second == 30:
        requests.post('https://prod-23.southeastasia.logic.azure.com:443/workflows/3e1c9c57e9714d59b2a735a4fb4493a3/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ZJJl-dVZLdRhlV5kDALwT98fkSwEcPWPqOr6GWjp_og',
                    json=data)