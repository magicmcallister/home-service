import os
from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import base64
from PIL import Image
import io

from config import Config
import postgres_client

config = Config()
config.load()

STORAGE_FOLDER = config.get("STORAGE", "PATH")
ADMIN_KEY = config.get("KEY", "ADMIN")

DB_HOST=config.get("DATABASE", "HOST")
DB_NAME=config.get("DATABASE", "NAME")
DB_USER=config.get("DATABASE", "USER")
DB_PASSWORD=config.get("DATABASE", "PASSWORD")

app = FastAPI()

###### Manage Users/Login Endpoints ######
class User(BaseModel):
	username: str
	password: str
	roles: list

class LoginUser(BaseModel):
	username: str
	password: str

apikey = APIKeyQuery(name="api_key")

async def get_api_key(apikey: str = Security(apikey)):
    if apikey == ADMIN_KEY:
	    return apikey
    else:
        raise HTTPException(
            status_code=403, detail="Missing authentication"
        )

async def get_user_by_key(apikey: str = Security(apikey)):
	if not apikey:
		raise HTTPException(
            status_code=403, detail="Missing authentication"
        )
	else:
		db = postgres_client.DbClient(
			DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
		)
		query = f"select username from sync_user where apikey = '{apikey}'"
		user = db.execute_query(query, select=True)
		if not user:
			raise HTTPException(
			status_code=404, detail="User not found"
		)
		else:
			return user

@app.get("/get_users")
async def get_users(api_key: APIKey = Depends(get_api_key)):
	db = postgres_client.DbClient(
		DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
	)
	users = db.execute_query("select username, password from sync_user", select=True)
	return users

@app.post("/login")
async def login(user: LoginUser, api_key: APIKey = Depends(get_api_key)):
	db = postgres_client.DbClient(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
	query = f"select u.username, u.password, u.apikey, r.role from sync_user u join user_role ur on u.id = ur.user_id join role r on ur.role_id = r.id where username = '{user.username}'"
	db_user = db.execute_query(query, select=True)
	#check_pass = bcrypt.checkpw(user.password.encode('utf-8'), user.password.encode('utf-8'))
	if not db_user:
		raise HTTPException(
			status_code=404, detail="User not found"
		)
	else:
		if not user.password == db_user[0][1]:
			raise HTTPException(
				status_code=403, detail="Could not validate credentials"
			)
	return db_user

###### Sync Images Endpoints ######
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
async def getfiles(folder: str, user: str = Depends(get_user_by_key)):
	files = os.listdir(STORAGE_FOLDER + f"/{folder}")
	print(user)
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
