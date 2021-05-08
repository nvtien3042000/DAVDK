import requests
from datetime import datetime

dt_string = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
print(dt_string)

##url = "http://localhost:8089/garage-management/history/add"
##
##payload={'is_out': 'false',
##'vehicle_id': '51F88838',
##'time': '2021-3-30 20:36:02'}
##files=[
##  ('image',('1.jpg',open('G:/DAVDK/1.jpg','rb'),'image/jpeg'))
##]
##headers = {}
##
##response = requests.request("POST", url, headers=headers, data=payload, files=files)
##
##print(response.text)


##import requests
##
##url = "http://localhost:8083/garage-management/vehicle/check-invalid?number_plate=511F88838"
##
##payload={}
##headers = {}
##
##response = requests.request("GET", url, headers=headers, data=payload)
##if response.status_code == 200:
##        print(response.status_code)
