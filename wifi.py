from network import WLAN
import socket
import machine
import os
import urequests

wlan = WLAN(mode=WLAN.STA)

def wifiSetup(name,pwd):
    nets = wlan.scan()
    found = False

    while not found:
        for net in nets:
            print(net.ssid)
            if net.ssid == name:
                print('Network found!')
                wlan.connect(net.ssid, auth=(net.sec, pwd), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                print('WLAN connection succeeded!')
                found = True
                break

