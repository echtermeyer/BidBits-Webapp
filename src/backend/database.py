import json
import psycopg2

from pathlib import Path

# Datenbank 'bidbits' muss manuell angelegt werden bevor der dump durchgeführt werden kann.

class Database:
    def __init__(self):
        self.__conn = None
        self.__cur = None

    def __connect(self):
        path_secrets = Path("src/secrets.json")
        with path_secrets.open() as f:
            secrets = json.load(f)

        self.__conn = psycopg2.connect(
            dbname=secrets["POSTGRES"]["DBNAME"],
            user=secrets["POSTGRES"]["USER"],
            password=secrets["POSTGRES"]["PASSWORD"],
            host=secrets["POSTGRES"]["HOST"],
            port=secrets["POSTGRES"]["PORT"]
        )

        self.__cur = self.__conn.cursor()

    def __disconnect(self):
        self.__conn.commit()
        self.__cur.close()
        self.__conn.close()

    def connection_manager(func):        
        def wrapper(self, *args, **kwargs):
            self.__connect()
            func(self, *args, **kwargs)
            self.__disconnect()

        return wrapper

    @connection_manager
    def database_dump(self):
        self.__cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        table_names = self.__cur.fetchall()

        if table_names.__len__() != 0:
            print("Deleting current tables and domains")
            for table in table_names:
                self.__cur.execute(f'DROP TABLE "{table[0]}" CASCADE;')
            self.__cur.execute("DROP DOMAIN IF EXISTS EMAIL")
            self.__cur.execute("DROP DOMAIN IF EXISTS PAYMENT_TYPE")

        print("Creating new tables")
        with open("./src/backend/ddl.sql", "r") as sql_file:
            sql = sql_file.read()
            print(sql)
            self.__cur.execute(sql)
            
        self.__cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        print(f"\n == Successfully Created Tables == \n{[x[0] for x in self.__cur.fetchall()]}\n")
  


db = Database()
db.database_dump()
