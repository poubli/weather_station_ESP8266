import socket
import datetime
from datetime import datetime
import pytz
import threading
import sqlite3

# FOR USE NEED TO SET THE PATH TO THE DATABASE AS self.DB_PATH.
# DB NEEDS TO BE CREATED FIRST
# RUN THE FILE ON RPi as threaded server

class server_meteo(threading.Thread):


    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.PORT = PORT

        ########## !!!!!! ##############
        # Set the path to the database here
        self.DB_PATH = '/Path/my_database'


    def run(self):

        while True:
            try:
                # RUN SERVER TO WAIT FOR Esp8266 weather station request
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind(('', self.PORT))
                self.server.settimeout(10)

                self.server.listen(5)
                self.data = {}
                local = pytz.timezone("Europe/Paris")

                # on getting request, separate request withe the ;
                self.client, infosClient = self.server.accept()
                self.requete = self.client.recv(1024)
                self.requete = self.requete.decode("utf-8")
                print(self.requete)

                values = self.requete.split(';')
                #print(values)
                temp_dht = float(values[0])
                temp_bme = float(values[1])
                pressure = float(values[2])
                humidity = float(values[3])

                date1=datetime.today()

                # Writing in DB

                connection=sqlite3.connect(self.DB_PATH)
                cursor=connection.cursor()
                a='INSERT INTO meteo(dht_temp, bme_temp, pressure, humidity, year, month, day, hour, minutes, date) VALUES(?,?,?,?,?,?,?,?,?,?)'
                cursor.execute(a, (temp_dht, temp_bme, pressure, humidity, date1.year, date1.month, date1.day, date1.hour, date1.minute, date1))
                connection.commit()
                cursor.close()
                connection.close()
                print('ok for database', values)


            except Exception as e:
                print(e)

                try:
                    self.client.close()

                except:
                    pass
            self.server.close()

#create instace of listening server on port 40000
a = server_meteo(40000)
a.start()
