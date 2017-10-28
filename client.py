import requests
import RPi.GPIO as GPIO
import time
import sys
import subprocess
from socket import *

# Set input GPIO
INPUT_GPIO = 37

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_GPIO, GPIO.IN)

# Global defines
DEFAULT_TIME_OUT = 60#120 # in seconds

# Room name
ROOM_NAME = ''

# SERVER DATA
CONNECTION_STRING= 'http://10.5.5.25:5000/update_movement'

# VIDEO_PATH
#VIDEO_PATH = "my_video.avi"

def send_message(status):
    i = 0
    p = subprocess.Popen(("fswebcam","-q","-r 640x480","1.jpg"))
    p.wait()


    f = open("1.jpg","rb")
    byteData = f.read()
    byteData = str(byteData).encode('base64','strict')
    
    dictionaryToSend = { 'name': ROOM_NAME , 'status' : str(status),
                          'image' : str(byteData)}
    f.close()
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
            send_message(int(isTaken))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python client.py -ROOM_NAME")
    else:
        ROOM_NAME = sys.argv[1]
        send_movement()
