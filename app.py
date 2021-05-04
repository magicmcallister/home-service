import os
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import base64
from PIL import Image
import io


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

STORAGE_FOLDER = os.environ.get("STORAGE_FOLDER")

class User(BaseModel):
	username: str
	password: str
	role: str

class UploadImage(BaseModel):
	dest_folder: str
	image: str
	image_name: str

@app.get("/", response_class=HTMLResponse)
async def main():
	content = """
	<!DOCTYPE html>
	<html>
	<head>
	<title>Havana - API</title>
	</head>
	<body>
	<center><p style="font-size:70px">Havana - API</p></center>
	</body>
	</html>
	"""
	return HTMLResponse(content=content, status_code=200)

@app.get("/get_storage_files/{folder}")
async def getfiles(folder: str):
	files = os.listdir(STORAGE_FOLDER + f"/{folder}") 
	return files

@app.post('/upload_file')
async def uploadfile(image_data: UploadImage):
	dest_folder = image_data.dest_folder
	im_64 = image_data.image
	im_name = image_data.image_name
	im = base64.b64decode(im_64.encode("utf-8"))
	img = Image.open(io.BytesIO(im))
	save_folder = STORAGE_FOLDER + "/" + dest_folder + "/" + im_name
	img.save(save_folder)
	return "Image Uploaded"
