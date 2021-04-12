import os
import requests
import json
import base64


def run():
    url = "http://127.0.0.1:5000/uploadfile"
    image = "/home/sr/storage/chat/avatar.png"

    path, filename = os.path.split(image)

    with open(image, "rb") as i:
        im = i.read()

    im_64 = base64.b64encode(im).decode("utf8")

    headers = {"Content-type": "application/json"}
    payload = json.dumps({
        "image": im_64,
        "image_name": filename,
        "dest_folder": "camera"
    })

    r = requests.post(url, data=payload, headers=headers)
    r.raise_for_status()
