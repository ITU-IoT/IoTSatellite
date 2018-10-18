# main.py -- put your code here!

from network import Bluetooth
import ubinascii
import json
import time
from datatypes import Device
import _thread
import urequests
from requests import get,post

ID = "KUKUK"
BT = Bluetooth()
DEVICE_RESET_TIME = 60 #seconds
HUB_IP = "192.168.43.128"
HUB_PORT = 5000
POST_PATH = "/sensor/beacon"
GET_PATH = "/sensor/beacon/device"
REQUEST_SLEEP_TIME = 1 #seconds

outlook_devices = []
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
            mac = ubinascii.hexlify(adv.mac,":")
            if name is not None and any((name == d['name']) for d in outlook_devices): #Should be mac address, but the tool we are using on the phone keeps changing the mac address.
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

def postDevices():
    while True:
        time.sleep(REQUEST_SLEEP_TIME)
        print(getDevicesJSON())
        data = {"id": ID, "devices": getDevicesJSON()}
        post(HUB_IP, HUB_PORT, POST_PATH, data)

def getDevices():
    global outlook_devices
    while True:
        time.sleep(REQUEST_SLEEP_TIME)
        r = get(HUB_IP, HUB_PORT, GET_PATH)
        if r is None:
            continue
        deviceJson = json.loads(r.text)
        print(outlook_devices)
        if 'devices' not in deviceJson:
            print("Request succeeded, but response was insufficient")
            continue
        outlook_devices = deviceJson['devices']


_thread.start_new_thread(postDevices, ())
_thread.start_new_thread(scan, ())
_thread.start_new_thread(getDevices, ())