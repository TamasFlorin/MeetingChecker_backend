from flask import Flask, request, jsonify

app = Flask(__name__)

rooms_hash = {}

@app.route("/update_movement", methods = ["POST"])
def update_movement():
	global rooms_hash

	content = request.get_json(silent=True)
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

	rooms_str = ""

	for key in rooms_hash:
		rooms_str += key
		rooms_str += ","
		rooms_str += rooms_hash[ key ]
		rooms_str += ";"

	return rooms_str;

if __name__ == "__main__":
	app.run(host='0.0.0.0')
