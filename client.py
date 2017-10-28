import requests
import RPi.GPIO as GPIO
import time
import sys

# Set input GPIO
INPUT_GPIO = 37

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_GPIO, GPIO.IN)

# Global defines
DEFAULT_TIME_OUT = 120 # in seconds

# Room name
ROOM_NAME = 'FARCASESTI'

# SERVER DATA
CONNECTION_STRING = 'http://10.5.5.25:5000/update_movement'

def send_message(status):
    dictionaryToSend = { 'name': ROOM_NAME , 'status' : str(status) }
    sendResult = requests.post(CONNECTION_STRING,json=dictionaryToSend)
    print('Reponse from server:',sendResult.text)

def send_movement():
    lastMovement = 0
    start = time.time()
    
    send_message(0) # Initially room state is 0
    
    while True:
        isMoving = GPIO.input(INPUT_GPIO)
        
        if isMoving == 1:
            lastMovement = time.time()
            print("Rick is moving")
            
        isTaken = ( time.time() - lastMovement ) <= DEFAULT_TIME_OUT
        
        if time.time() - start >= DEFAULT_TIME_OUT:
            start = time.time()
            send_message(int(isTaken))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python client.py -ROOM_NAME")
    else:
        ROOM_NAME = sys.argv[1]
        send_movement()
