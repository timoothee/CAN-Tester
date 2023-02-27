import os

class CanModule():
    def __init__(self, txquelen = 1000, baudrate = 1000000, dbaudrate = 8000000):
        self.can_send_module_name = ""
        self.can_receive_module_name = ""
        self.txquelen = txquelen
        self.baudrate = baudrate
        self.dbaudrate = dbaudrate
        self.frame_que = []

    def set_can_send_module_name(self, name):
        self.can_send_module_name = name
        print(self.can_send_module_name)

    def set_can_receive_module_name(self, name):
        self.can_receive_module_name = name
        print(self.can_receive_module_name)

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def get_baudrate(self):
        return self.baudrate
    
    def set_dbaudrate(self, dbaudrate):
        self.dbaudrate = dbaudrate

    def get_dbaudrate(self):
        return self.dbaudrate
    
    def interface_up(self):
        os.popen(f"sudo ip link set {self.can_send_module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on")
        pass

    def interface_down(self):
        os.popen(f"candump {self.name}")
        pass

    def add_frame_to_que(self, frame):
        self.frame_que.append(frame)


    def get_name(self):
        return self.can_send_module_name

    def send_q(self):
        for message in self.frame_que:
            os.popen(f"cansend {self.can_send_module_name} {message}")