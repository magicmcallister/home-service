import os

from pydantic import BaseModel
from fastapi import FastAPI, Security, HTTPException, UploadFile, Depends
from fastapi.security.api_key import APIKeyQuery, APIKey
from fastapi.responses import HTMLResponse
import shutil
from typing import List

import config
import models


STORAGE_FOLDER = config.get_env("STORAGE_PATH")

app = FastAPI()


# Basic authentication
apikey = APIKeyQuery(name="api_key")


async def check_apikey(apikey: str = Security(apikey)):
    if apikey == config.get_env("KEY_ADMIN"):
        return apikey
    else:
        raise HTTPException(status_code=403, detail="Wrong authorization")


# Base Models
class Folder(BaseModel):
    user_id: int
    name: str


@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
	<!DOCTYPE html>
	<html>
	<head>
	<title>Havana - API</title>
	</head>
	<body>
	<center><p style="font-size:60px">Havana - API</p></center>
	</body>
	</html>
	"""
    return HTMLResponse(content=content, status_code=200)


@app.get("/files/{user_id}")
async def get_files(user_id: int, api_key: APIKey = Depends(check_apikey)):
    user_path = STORAGE_FOLDER + f"/{user_id}"
    user_files = {}
    if os.path.exists(user_path):
        for root, dirs, files in os.walk(user_path):
            for name in dirs:
                user_files[name] = []
            for name in files:
                folder = root.split("/")[-1]
                user_files[folder].append(f"{root}/{name}")
    else:
        raise HTTPException(status_code=404, detail="User folder not found")
    return user_files


@app.post("/files/upload")
async def create_upload_files(files: List[UploadFile], api_key: APIKey = Depends(check_apikey)):
    for file in files:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"filenames": [file.filename for file in files]}


@app.get("/folders/{user_id}")
async def get_folders(user_id: int, api_key: APIKey = Depends(check_apikey)):
    user_path = STORAGE_FOLDER + f"/{user_id}"
    if os.path.exists(user_path):
        files = os.listdir(user_path)
    else:
        raise HTTPException(status_code=404, detail="User folder not found")
    return files


@app.post("/folders")
async def post_folders(data: Folder, api_key: APIKey = Depends(check_apikey)):
    user_id = data.user_id
    folder_name = data.name

    user_path = STORAGE_FOLDER + f"/{user_id}"
    if os.path.exists(f"{user_path}/{folder_name}"):
        return f"{folder_name} is already created for user: {user_id}"
    else:
        os.makedirs(f"{user_path}/{folder_name}")
        return f"Succesful folder creation: {folder_name}"


# @app.get("/light_info")
# async def light_info():
#     return controller.get_info()


# @app.post("/light_on")
# async def light_on():
#     controller.turn_on()
#     return "Success"


# @app.post("/light_off")
# async def light_off():
#     controller.turn_off()
#     return "Success"
