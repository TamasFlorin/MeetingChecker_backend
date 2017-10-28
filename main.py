from flask import Flask
from threading import Thread,Lock
import RPi.GPIO as GPIO
import time
app = Flask(__name__)

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
INPUT_GPIO = 37
GPIO.setup(INPUT_GPIO, GPIO.IN)

# movement stuff
last_movement=0
mutex = Lock()
DEFAULT_TIME_OUT = 300

@app.route("/get_movement")
def get_movement():
	global last_movement,mutex

	mutex.acquire()
	time_diff = time.time() - last_movement
	print(time_diff)
	mutex.release()

	if time_diff <= DEFAULT_TIME_OUT:
		return "1"

	return "0"

	#return flag

def check_movement():
        global last_movement,mutex,GPIO
        i = 0
        while True:
                i = GPIO.input(INPUT_GPIO)
                if i == 1:
                        mutex.acquire()
                        print("Rick")
                        last_movement = time.time()
                        mutex.release()
                
                time.sleep(0.1)

def start_service():
	app.run(host='0.0.0.0')

if __name__ == "__main__":
	thread = Thread(target = check_movement)
	thread.start()
	start_service()
