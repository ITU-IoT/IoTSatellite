# main.py -- put your code here!

from network import Bluetooth
import ubinascii
import json
import time
from datatypes import Device
import _thread

ID = "KUKUK"
BT = Bluetooth()
RESET_TIME = 3600 #seconds
devices = {}

def getDevicesJSON():
    res = {}
    for key, val in devices.items():
        res[key] = json.dumps(val.__dict__)
    return json.dumps(res)

def clearOldDevices():
    for key,val in devices.items():
        cur_time = int(time.time())
        if(cur_time-val.discovery_time > RESET_TIME):
            del devices[key]


def scan():
    BT.start_scan(-1)
    while BT.isscanning():
        adv = BT.get_adv()
        if adv:
            name = BT.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            if name is not None:
                mac = ubinascii.hexlify(adv.mac,":")
                rssi = adv.rssi
                cur_time = int(time.time())
                d = Device(mac, name, rssi, cur_time)
                devices[mac] = d
            # print(name)
            # print("RSSI: %d " % rssi)
            # print("MAC: %s" % mac)
            # print(json.dumps(d.__dict__))

        clearOldDevices()
        print(getDevicesJSON())

def test():
    while True:
        print("HAHAHAHAHAHAHAHAHAHAAHA")

_thread.start_new_thread(test, ())
_thread.start_new_thread(scan, ())