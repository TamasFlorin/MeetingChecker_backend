'''
Created on Oct 28, 2016
@author: Bogdan Boboc (bogdanboboc97@gmail.com) && Florin Tamas (tamasflorin@live.com) 
'''

import requests
import RPi.GPIO as GPIO
import time
import sys
import subprocess
from socket import *
import Adafruit_DHT as dht

# Set input GPIO
INPUT_GPIO = 37
INPUT_TEMPERATURE_GPIO = 23

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_GPIO, GPIO.IN)
#GPIO.setup(INPUT_TEMPERATURE_GPIO, GPIO.IN)

# Global defines
DEFAULT_TIME_OUT = 120 # in seconds

# Room name
ROOM_NAME = ''

# SERVER DATA
CONNECTION_STRING= 'http://10.5.5.25:5000/update_movement'

# VIDEO_PATH
#VIDEO_PATH = "my_video.avi"

# added as a last try to improve the final project
# do not mind this bullshit
def get_weather():
    h,t = dht.read_retry(dht.AM2302 ,INPUT_TEMPERATURE_GPIO)
    return h,t

def get_image_data():
    p = subprocess.Popen(("fswebcam","-q","-r 640x480","1.jpg"))
    p.wait()
    f = open("1.jpg","rb")
    byteData = f.read()
    byteData = str(byteData).encode('base64','strict')
    f.close()
    return byteData

def send_message(status):
    h,t = get_weather()
    humidity = str(h)
    temperature = str(t)
    image = get_image_data()
    
    dictionaryToSend = { 'name': ROOM_NAME , 'status' : str(status),
                         'image' : str(image),'humidity': humidity,
                         'temperature' : temperature
                        }
   
    sendResult = requests.post(CONNECTION_STRING,json=dictionaryToSend)
    
    print('Reponse from server:',sendResult.text)

def send_movement():
    lastMovement = 0
    lastRoomState = 0
    start = time.time()
    
    send_message(0) # Initially room state is 0
    
    while True:
        isMoving = GPIO.input(INPUT_GPIO)
        
        if isMoving == 1:
            lastMovement = time.time()
            #print("Rick is moving")
            
        isTaken = ( time.time() - lastMovement ) <= DEFAULT_TIME_OUT
        
        if lastRoomState != isTaken or time.time() - start >=5:
            start = time.time()
            lastRoomState = isTaken
            try:
                send_message(int(isTaken))
            except:
                print("Got an exception!Retrying...")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python client.py -ROOM_NAME")
    else:
        ROOM_NAME = sys.argv[1]
        send_movement()

