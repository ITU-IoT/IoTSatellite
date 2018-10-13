# main.py -- put your code here!

from network import Bluetooth
import ubinascii
import json
import time
from datatypes import Device
import _thread
import urequests

ID = "KUKUK"
BT = Bluetooth()
DEVICE_RESET_TIME = 60 #seconds
POST_IP = "192.168.1.159"
POST_PORT = 5000
REQUEST_SLEEP_TIME = 10 #seconds

devices = {}

def getDevicesJSON():
    res = {}
    for key, val in devices.items():
        res[key] = json.loads(json.dumps(val.__dict__))
    return json.loads(json.dumps(res))

def clearOldDevices():
    for key,val in devices.items():
        cur_time = int(time.time())
        if(cur_time-val.discovery_time > DEVICE_RESET_TIME):
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
        #print(getDevicesJSON())

def post():
    while True:
        time.sleep(REQUEST_SLEEP_TIME)
        data = {"id": ID, "devices": getDevicesJSON()}
        print("Posting data to "+POST_IP+":"+str(POST_PORT)+":")
        print(data)
        try:
            r = urequests.post("http://"+POST_IP+":"+str(POST_PORT)+"/sensor/beacon", json = data)
            print("Response:")
            print(r.text)
        except Exception as e:
            print("Post failed! Error message:")
            print(repr(e))

_thread.start_new_thread(post, ())
_thread.start_new_thread(scan, ())