import sqlite3
db_path="my_path"
connection=sqlite3.connect(db_path)
cursor=connection.cursor()

req_create="""CREATE TABLE ruche_00
               (id INTEGER PRIMARY KEY AUTOINCREMENT, dht_temp REAL, dht_hum REAL, temp_couvin REAL, poids REAL, year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minutes INTEGER, date DATETIME)"""


cursor.execute(req_create)
connection.commit()
connection.close()
