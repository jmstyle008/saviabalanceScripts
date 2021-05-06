import psycopg2


class dbConnect:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="postgres", user='postgres', password='root', host='127.0.0.1', port='5432'
        )
        self.cursor = self.conn.cursor()

    def getVersion(self):
        return self.cursor.execute("select version()")

    def runQuery(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insertQuery(self, query):
        self.cursor.execute(query)
        self.conn.commit()
