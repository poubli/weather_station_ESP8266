# weather_station_ESP8266

This simple weather station use BME280 and DHT11 sensors to collect outdoor temp/humidity and pressure

The weather station is powered with 18650 Lithium battery charged by a solar panel.
(Up to date this station is on my window for 2 years without any need to manually charge the battery even in winter.)

Esp8266 wakeup every hour, collect data and send them through local network to a RPi implementing an IP SERVER (see RPi part of this project).
RPi get data and store them into SQLlite database.
Another part of RPi program serve a local webserver to display real time and historic of measurements (see "coming soon on my git")

Additionally the esp8266 connect also to ESP32 wich serve it's own IP SERVER.
ESP32 display collected weather data with TFT LCD display (see "coming soon on my git")

# Usage
BME is connected to SCL / SDA i2c esp pins
DHT is connected to IO 14
Weather station shall be installed outdoor where wifi is available (so not to far)
First install my_env library and fill the env.json file (see env.json.example.json file)
this can work either with or without ESP32 display.

# Easy EDA PCB 
![Capture d’écran 2022-09-19 à 20 07 53](https://user-images.githubusercontent.com/109547086/191084801-ef04af7f-2880-4805-b063-bc54d9ed5b57.png)
