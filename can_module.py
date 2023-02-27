import os

class CanModule():
    def __init__(self, txquelen = 1000, baudrate = 1000000):
        self.name = ""
        self.txquelen = txquelen
        self.baudrate = baudrate
        self.frame_que = []

    def set_baudrate(self):
        os.popen(f"sudo ip link set can0 type can bitrate {self.baudrate}")

    def interface_up(self):
        os.popen(f"sudo ip link set up {self.name}")
        pass

    def interface_down(self):
        os.popen(f"sudo ip link set down {self.name}")
        pass

    def add_frame_to_que(self, frame):
        self.frame_que.append(frame)

    def set_name(self, name):
        self.name = name
        print(self.name)

    def get_name(self):
        return self.name