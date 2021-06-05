import os
from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import datetime
import base64
from PIL import Image
import io
import secrets

from config import Config
import postgres_client
from light_controller import LightController

config = Config()
config.load()

STORAGE_FOLDER = config.get("STORAGE", "PATH")
ADMIN_KEY = config.get("KEY", "ADMIN")

DB_HOST=config.get("DATABASE", "HOST")
DB_NAME=config.get("DATABASE", "NAME")
DB_USER=config.get("DATABASE", "USER")
DB_PASSWORD=config.get("DATABASE", "PASSWORD")

app = FastAPI()

controller = LightController()

##### Aux Functions #####
def _generate_apikey():
	return secrets.token_urlsafe(25)

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
			return user[0][0]

@app.get("/roles")
async def get_roles(api_key: APIKey = Depends(get_user_by_key)):
	db = postgres_client.DbClient(
		DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
	)
	roles = db.execute_query("select id, role from role", select=True)
	return roles

@app.post("/new_user")
async def post_user(user: User, api_key: APIKey = Depends(get_user_by_key)):
	db = postgres_client.DbClient(
		DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
	)
	generated_apikey = _generate_apikey()
	user_query = f"insert into sync_user(username, password, apikey) values ('{user.username}', '{user.password}', '{generated_apikey}')"
	db.execute_query(user_query)
	user_id_query = f"select id from sync_user where username = '{user.username}'"
	user_id = db.execute_query(user_id_query, select=True)
	for role_id in user.roles:
		role_query = f"insert into user_role(user_id, role_id) values ({user_id[0][0]}, {role_id})"
		db.execute_query(role_query)
	return "New user has been created"

@app.get("/users")
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
	user_path = STORAGE_FOLDER + f"/{user}" + f"/{folder}"
	if os.path.exists(user_path):
		files = os.listdir(user_path)
	else:
		os.makedirs(user_path)
		files = os.listdir(user_path)
	return files

@app.post('/upload_file')
async def uploadfile(image_data: UploadImage, user: str = Depends(get_user_by_key)):
	dest_folder = image_data.dest_folder
	im_64 = image_data.image
	im_name = image_data.image_name
	im = base64.b64decode(im_64.encode("utf-8"))
	img = Image.open(io.BytesIO(im))
	save_folder = STORAGE_FOLDER + "/" + user + "/" + dest_folder + "/" + im_name
	img.save(save_folder)
	return "Image Uploaded"

###### Light Controller Endpoint ######
def _check_light_controller():
	if abs((controller.last_update - datetime.datetime.now()).total_seconds()) > 1200:
		controller._restart()

@app.get('/light_info')
async def light_info(api_key: APIKey = Depends(get_api_key)):
	_check_light_controller()
	return controller.get_info()

@app.post('/light_on')
async def light_on(api_key: APIKey = Depends(get_api_key)):
	_check_light_controller()
	controller.turn_on()
	return "Success"

@app.post('/light_off')
async def light_off(api_key: APIKey = Depends(get_api_key)):
	_check_light_controller()
	controller.turn_off()
	return "Success"
