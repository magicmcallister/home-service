from flask import Flask, jsonify, request
import os
import json
import base64
from PIL import Image
import io


app = Flask(__name__)

STORAGE_FOLDER = "/home/sr/storage"

@app.route('/test', methods=["GET"])
def main():
	return "MagicMcallister API"


@app.route('/getstoragefiles/<folder>', methods=['GET'])
def getfiles(folder):
	files = os.listdir(STORAGE_FOLDER + f"/{folder}") 
	return jsonify(files)

@app.route('/uploadfile', methods=['POST'])
def uploadfile():
	if request.method == "POST":
		data = json.loads(request.data)
		dest_folder = data["dest_folder"]
		im_64 = data["image"]
		im_name = data["image_name"]
		im = base64.b64decode(im_64.encode("utf-8"))
		img = Image.open(io.BytesIO(im))
		save_folder = STORAGE_FOLDER + "/" + dest_folder + "/" + im_name
		img.save(save_folder)
		return request.data

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')
