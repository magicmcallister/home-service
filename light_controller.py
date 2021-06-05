import json
import datetime
from PyP100 import PyP100


class LightController:
    def __init__(self):
        self.p100 = PyP100.P100("192.168.1.16", "sarablanco2a@gmail.com", "MF477WUuUtqi89Q")
        self.p100.handshake()
        self.p100.login()

        self.on_state = None
        self.last_update = datetime.datetime.now()

    def _restart(self):
        self.p100.handshake()
        self.p100.login()
        self.last_update = datetime.datetime.now()

    def turn_on(self):
        self.get_current_state()
        if self.on_state:
            pass
        else:
            self.p100.turnOn()
            self.on_state = True
    
    def turn_off(self):
        self.get_current_state()
        if self.on_state:
            self.p100.turnOff()
            self.on_state = False
        else:
            pass

    def get_current_state(self):
        device_info = json.loads(self.p100.getDeviceInfo())
        self.on_state = device_info["result"]["device_on"]

    def get_info(self):
        return json.loads(self.p100.getDeviceInfo())