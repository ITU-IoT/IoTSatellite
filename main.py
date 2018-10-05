# main.py -- put your code here!

from network import Bluetooth
import ubinascii
prevrssi = 1000

bl = Bluetooth()
bl.start_scan(5)

while bl.isscanning():
    adv = bl.get_adv()
    if adv:

        # try to get the complete name
        mac = ubinascii.hexlify(adv.mac,":")
        # rssi = ubinascii.hexlify(adv.rssi)
        rssi = "RSSI: %d         " % adv.rssi
        # if mac == "c0:ee:fb:d2:2d:24":
        #     print("found!")
        if abs(adv.rssi) < prevrssi:    
            hrssi = abs(adv.rssi)
            prevrssi = hrssi
            da = bl.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            print(da)
            print("RSSI: %d " % hrssi)
            print("MAC: %s" % mac)





        #print("MAC: "+ str(mac) + "         " + rssi)

        #print(bl.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
        #mfg_data = bl.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
        
        #if mfg_data:
            # try to get the manufacturer data (Apple's iBeacon data is sent here)
            #print(ubinascii.hexlify(mfg_data))