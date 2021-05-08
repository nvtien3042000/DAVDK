import cv2
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import requests
from webcamFindPlate import findPlate, find_plate_inf

#faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor")

def on_message(client, userdata, msg):
    
    print(msg.payload)
    src = msg.payload.decode('utf-8')
    print(src)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.137.1", 8900, 60)
oldPlate = 0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    x, y, w, h = findPlate(frame)
    
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('Video', frame)
    image=frame[y:y+h,x:x+w]
    if w/h > 2:
        image = cv2.resize(image, (470, 110))# 0:h
        
    else:
        image = cv2.resize(image, (315, 235))
    
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3,3), 0) # lam mo de giam gay nhieu
    # Ap dung threshold de phan tach so va nen
    binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    if w/h > 2:
        plate_info = find_plate_inf(binary, image, 1);
    else:
    
        h = int(image.shape[0]/2)
        p1 = binary[0:h,0:image.shape[1]]
        p2 = binary[h:image.shape[0],0:image.shape[1]]
        image_p1 = image[0:h,0:image.shape[1]]
        image_p2 = image[h:image.shape[0],0:image.shape[1]]

        plate_info = find_plate_inf(p1, image_p1, 1)
        plate_info = plate_info + find_plate_inf(p2, image_p2, 5)

    url = "http://localhost:8089/garage-management/vehicle/check-invalid?number_plate="+plate_info
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print("plate-----------------: ",plate_info)
    if(response.status_code == 200):
        print("plate: ",plate_info)
        client.publish("resultPlate",'1',qos = 0, retain = False)
        

        if oldPlate != plate_info:
            name = "historyImage.jpg"
            cv2.imwrite(name, frame)
            url = "http://localhost:8089/garage-management/history/add"
            dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(dt_string)
            payload={'is_out': 'false',
            'vehicle_id': plate_info,
            'time': dt_string}
            files=[
              ('image',('historyImage.jpg',open('G:/DAVDK/historyImage.jpg','rb'),'image/jpeg'))
            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

        oldPlate = plate_info
                

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)
#client.loop_forever()
video_capture.release()
cv2.destroyAllWindows()




