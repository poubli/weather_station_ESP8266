# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

from mpy_env import load_env, get_env, put_env

# LOAD ENV FILE AND VARIABLE, THIS FEATURES NEEDS TO HAVE INSTALLED
# mpy_env LIBRAIRY FIRST, USE "isntallation_lib.py" FILE

load_env()

SSID=get_env("SSID")
PWD=get_env("PWD")
IP=get_env("IP")
PORT=get_env("PORT")
IP2=get_env("IP2")
PORT2=get_env("PORT2")

#print(SSID,PWD, IP2, PORT2)

#CONNECT TO NETWORK
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PWD)

    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())

do_connect()
