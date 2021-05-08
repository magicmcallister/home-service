import psycopg2


class DbClient:
    def __init__(self, host, name, user, password):
        self.conn = psycopg2.connect(
            host=host, database=name, user=user, password=password
            )
        self.cur = self.conn.cursor()

    def _close_connection(self):
        self.conn.close()

    def execute_query(self, query, select=False):
        if select:
            try:
                self.cur.execute(query)
                return self.cur.fetchall()
            except Exception as e:
                print(f"Database Error: {e}")
        else:
            try:
                self.cur.execute(query)
                self.conn.commit()
            except Exception as e:
                print(f"Database Error: {e}")
