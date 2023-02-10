import os

class CanModule():
    def __init__(self, name, txquelen, baudrate):
        self.name = name
        self.txquelen = txquelen
        self.baudrate = baudrate

    def set_baudrate(self):
        os.popen(f"sudo ip link set can0 type can bitrate {self.baudrate}")

    def interface_up(self):
        os.popen(f"sudo ip link set up {self.name}")
        pass

    def interface_down(self):
        os.popen(f"sudo ip link set down {self.name}")
        pass