import psycopg2

import config

config.load()


DB_HOST=config.get("DATABASE", "HOST")
DB_NAME=config.get("DATABASE", "NAME")
DB_USER=config.get("DATABASE", "USER")
DB_PASSWORD=config.get("DATABASE", "PASSWORD")


class DbClient:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
        self.cur = self.conn.cursor()

