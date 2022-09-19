import machine
import bme280
import dht
import socket
from time import sleep
import network
from mpy_env import load_env, get_env, put_env

#This simple weather station use BME280 and DHT11 sensors to collect outdoor temp/humidity and pressure
# The weather station is powered with 18650 Lithium battery charged by a solar panel.
#(Up to date this station is on my window for 2 years without any need to manually charge the battery even in winter.)

#Esp8266 wakeup every hour, collect data and send them through local network to a RPi implementing an IP SERVER (see RPi part of this project).
# RPi get data and store them into SQLlite database.
# Another part of RPi program serve a local webserver to display real time and historic of measurements (see "coming soon on my git")

# Additionally the esp8266 connect also to ESP32 wich serve it's own IP SERVER.
# ESP32 display collected weather data with TFT LCD display (see "coming soon on my git")

#USAGE:
# BME is connected to SCL / SDA i2c esp pins
# DHT is connected to IO 14
# Weather station shall be installed outdoor where wifi is available (so not to far)
# First install my_env library and fill the env.json file (see env.json.example.json file)
# this can work either with or without ESP32 display.



def deep_sleep(msecs):
  # configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after X milliseconds (waking the device)
  rtc.alarm(rtc.ALARM0, msecs)
  # put the device to sleep
  machine.deepsleep()

def update_data():

    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
    bme = bme280.BME280(i2c=i2c)

    sensor_dht= dht.DHT11(machine.Pin(14))

# DO MULTIPLE CALL TO BME, LOOKS TO GUVE ACCURATE VALUE
    for i in range (10):
        print('i:', i)
        temp = bme.values[0]
        pressure= bme.values[1]

#CALL DHT TO MEASURE
    sensor_dht.measure()
    hum=sensor_dht.humidity()
    dht_temp= sensor_dht.temperature()


# CONNECT TO RPi VIA WIFI AND SEND DATA
# RPi IS SERVING A SOCKET SERVER WHO RECORDS SENT DATA INTO SQLlite DATABASE
# SEE RPi PART OF THIS PROJECT for SERVERMETEOCLASS.

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(10)

    try:
        s.connect((IP, int(PORT)))
        requete = str(dht_temp)+ ";" + temp.strip('C')+ ";"+pressure.strip('hPa')+ ';' + str(hum)
        sleep(1)
        s.send(requete.encode('utf-8'))
        print('sent to RPi')

        s.close()
        sleep(5)

    except Exception as e:
        print(e)
        s.close()
        with open ('log.txt', 'a') as monfichier:
            monfichier.write(str(e))

#CONNECT TO ESP32 METEO LCD VIEWER AND SEND DATA
#
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(10)
    try:
        print(IP2,PORT2)
        s.connect((IP2, int(PORT2)))
        sleep(2)
        requete = str(dht_temp,)+ ";" + str(round(float(temp.strip('C')),1))+" °C"+";"+  ";" + str(round(float(pressure.strip('hPa')),0))+" hPa"+ ';' + str(round(hum,1)) +" %"+';'
        s.send(requete.encode('utf-8'))
        sleep(1)
        print('sent to ESP32')

        #Wait for server response to say everything ok
        rep=s.recv(1024).decode("utf-8");
        print("rep",rep)

        s.close()


    except Exception as e:
        print(e)
        s.close()
        with open ('log.txt', 'a') as monfichier:
            monfichier.write(str(e))


    #print('Im awake, but Im going to sleep')


update_data()
# deepsleep for 1 hour
deep_sleep(3600000)
