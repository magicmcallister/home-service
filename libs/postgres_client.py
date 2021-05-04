import psycopg2

import config

config.load()

DB_HOST=config.get("database", "host")
DB_NAME=config.get("database", "name")
DB_USER=config.get("database", "user")
DB_PASSWORD=config.get("database", "password")


class DbClient:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
        self.cur = self.conn.cursor()