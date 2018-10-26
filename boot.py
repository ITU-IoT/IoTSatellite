# boot.py -- run on boot-up
from network import WLAN
import pycom
from wifi import wifiSetup

SSID = "NETGEAR"
PWD = "hackerMAN158"

pycom.heartbeat(False)
pycom.rgbled(0xff7f00)
wifiSetup(SSID, PWD)
pycom.rgbled(0x00ff00)
