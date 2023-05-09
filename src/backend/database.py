import json
import psycopg2

from pathlib import Path


path_secrets = Path("src/secrets.json")
with path_secrets.open() as f:
    secrets = json.load(f)


conn = psycopg2.connect(
    dbname=secrets["POSTGRES"]["DBNAME"],
    user=secrets["POSTGRES"]["USER"],
    password=secrets["POSTGRES"]["PASSWORD"],
    host=secrets["POSTGRES"]["HOST"],
    port=secrets["POSTGRES"]["PORT"]
)

cur = conn.cursor()
cur.execute("""SELECT * FROM user """)

rows = cur.fetchall()
if not len(rows):
    print("Empty")

for row in rows:
    print(row)

cur.close()
conn.close()