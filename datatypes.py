
class Device:
    def __init__(self, mac, name, rssi, discovery_time):
        self.mac = mac
        self.name = name
        self.rssi = rssi
        self.discovery_time = discovery_time