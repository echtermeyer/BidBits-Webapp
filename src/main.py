import psycopg2

conn = psycopg2.connect(
    dbname="bidbits",
    user="docker",
    password="docker",
    host="0.0.0.0",
    port="8080"
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