'''
Created on Oct 28, 2016
@author: Bogdan Boboc (bogdanboboc97@gmail.com) && Florin Tamas (tamasflorin@live.com) 
'''

from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

rooms_hash = {}
persons_count_hash = {}
humidity_hash = {}
temperature_hash = {}

def get_number_of_persons(image_path):
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	capture = cv2.imread(image_path)
	found,w = hog.detectMultiScale(capture,winStride=(8,8),padding=(32,32),scale=1.05)
	return len(found)

@app.route("/update_movement", methods = ["POST"])
def update_movement():
	global rooms_hash

	content = request.get_json(silent = True)
	response = {}

	try:
		rooms_hash[ content["name"] ] = content["status"]

		humidity_hash[ content["name"] ] = content["humidity"]

		temperature_hash[ content["name"] ] = content["temperature"]

		save_image(content["name"], str(content["image"]).decode('base64'))

		result = get_number_of_persons(content["name"] + ".jpeg")

		update_persons_count(content["name"], result)

		response = { "status" : "ok" }
	except:
		response = { "status" : "invalid data" }

	return jsonify(response)

def update_persons_count(room, count):
	global persons_count_hash

	if room not in persons_count_hash.keys():
		persons_count_hash[room] = []

	if len(persons_count_hash[room]) >= 6:
		persons_count_hash[room] = persons_count_hash[room][1:]

	persons_count_hash[room].append(count)

@app.route("/get_movement", methods = ["GET"])
def get_movement():
	global rooms_hash
	return get_rooms_CSV()

@app.route("/get_movement_json", methods = ["GET"])
def get_movement_json():
	global rooms_hash

	return get_rooms_JSON()

@app.route("/get_room_status", methods = ["GET", "POST"])
def get_room_status():
	global rooms_hash
	try:
		room_name = request.args.get("name")

		if room_name in rooms_hash.keys():
			return jsonify( { "status" : "" + rooms_hash[ room_name ] , "count" : get_persons_count(room_name), "humidity" : humidity_hash[room_name], "temperature" : temperature_hash[room_name] } )
	except:
		return jsonify( { "status" : "Bad format!" })
	return jsonify( { "status" : "Room inexistent!"} )

def get_rooms_JSON(): 
	global rooms_hash

	rooms_json = []

	for room_name in rooms_hash:
		rooms_json.append( { "name" : room_name, "status" : rooms_hash[ room_name ], "count" : get_persons_count(room_name), "humidity" : humidity_hash[room_name], "temperature" : temperature_hash[room_name] } )

	return jsonify(rooms_json)

def get_persons_count(room_name):
	global persons_count_hash

	sum = 0

	for count in persons_count_hash[room_name]:
		sum += count

	return str( int( round(sum / 6) ) )

def get_rooms_CSV():
	global rooms_hash

	rooms_CSV = ""

	for key in rooms_hash:
		rooms_CSV += key
		rooms_CSV += ","
		rooms_CSV += rooms_hash[ key ]
		rooms_CSV += ","
		rooms_CSV += get_persons_count(key)
		rooms_CSV += ","
		rooms_CSV += humidity_hash[ key ]
		rooms_CSV += ","
		rooms_CSV += temperature_hash[ key ]
		rooms_CSV += ";"

	return rooms_CSV

def save_image(room_name, str_image):
	photo_file_name = room_name + ".jpeg"
	file = open(photo_file_name, "wb")
	file.write(str_image)
	file.close()

if __name__ == "__main__":
	app.run(host='0.0.0.0',threaded=True)
