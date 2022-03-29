# Home Service API


- [Home Service API](#home-service-api)
  - [Overview](#overview)
  - [Configuration](#configuration)
  - [Endpoints](#endpoints)
  - [How to run](#how-to-run)
  - [Future work](#future-work)

## Overview

API to serve same functions to interact with external apps to connect them to a local storage.
One of the uses can be to create a personal file backup cloud.

## Configuration

Follow [env template](.env_template) file.

## Endpoints

- files/{user_id} --> Get storage folder and files structure by user.
- files/upload --> Post files (WIP).
- folders/{user_id} --> Get storage folders by user.
- folders --> Post folder by user.

## How to run

Tutorial from [FastAPI docs](https://fastapi.tiangolo.com/deployment/manually/)

- uvicorn main:app --host 0.0.0.0 --port 8000

## Future work

- Light controller endpoints
- Dockerize app
