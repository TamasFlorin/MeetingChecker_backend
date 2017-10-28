from flask import Flask
from threading import Threading,Lock

app = Flask(__name__)

last_movement=0
mutex = Lock()
DEFAULT_TIME_OUT = 5000

@app.route("/get_movement")
def get_movement():
	global last_movement,mutex

	mutex.acquire()
	time_diff = time.time() - last_movement()
	mutex.release()

	if time_diff <= DEFAULT_TIME_OUT:
		return "1"

	return "0"

	#return flag

def check_movement():
	global last_movement,mutex
	i = 0
	while True:
		if i == 1:
			mutex.acquire()
			last_movement = time.time()
			mutex.release()

		time.sleep(0.1)

def start_service():
	app.run(host='0.0.0.0')

if __name__ == "__main__":
	thread = Thread(target = check_movement)
	thread.start()
	start_service()
