from flask import Flask, request, jsonify

app = Flask(__name__)

rooms_hash = {}

@app.route("/update_movement", methods = ["POST"])
def update_movement():
	global rooms_hash

	content = request.get_json(silent = True)
	response = {}

	try:
		rooms_hash[ content["name"] ] = content["status"]
		print (content["name"] + " set as " + content["status"])
		response = { "status" : "ok" }
	except:
		response = { "status" : "invalid data" }

	return jsonify(response)

@app.route("/get_movement", methods = ["GET"])
def get_movement():
	global rooms_hash

	return get_rooms_CSV();


@app.route("/get_movement_json", methods = ["GET"])
def get_movement_json():
	global rooms_hash

	return get_rooms_JSON();

@app.route("/get_room_status", methods = ["GET", "POST"])
def get_room_status():
	global rooms_hash
	try:
		room_name = request.args.get("name")

		if room_name in rooms_hash.keys():
			return jsonify( { "status" : "" + rooms_hash[ room_name ] } )
	except:
		return jsonify( { "status" : "Bad format!" })
	return jsonify( { "status" : "Room inexistent!"} )

def get_rooms_JSON(): 
	global rooms_hash

	rooms_json = []

	for room_name in rooms_hash:
		rooms_json.append( { "name" : room_name, "status" : rooms_hash[ room_name ] } )

	return jsonify(rooms_json)

def get_rooms_CSV():
	global rooms_hash

	rooms_CSV = ""

	for key in rooms_hash:
		rooms_CSV += key
		rooms_CSV += ","
		rooms_CSV += rooms_hash[ key ]
		rooms_CSV += ";"

	return rooms_CSV

if __name__ == "__main__":
	app.run(host='0.0.0.0')
