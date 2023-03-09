import os

class CanModule():
    def __init__(self, txquelen = 1000, baudrate = 1000000, dbaudrate = 5000000):
        self.txquelen = txquelen
        self.baudrate = ""
        self.dbaudrate = ""
        self.frame_que = []
        self.module_name = ""

    def set_module_name(self, name):
        self.module_name = name
    
    def get_can_module_name(self):
        return self.module_name
    
    #baudrate
    def set_baudrate(self, baudrate):
        self.baudrate = baudrate

    def get_baudrate(self):
        return self.baudrate
    
    #dbaudrate
    def set_dbaudrate(self, dbaudrate):
        self.dbaudrate = dbaudrate

    def get_dbaudrate(self):
        return self.dbaudrate
    
    def interface_up(self):
        os.popen(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on", 'w',1)
        print(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on")
        
    def can_dump(self):
        os.popen(f"candump {self.module_name} > can.log", "w")
        print("---")

    def interface_down(self):
        os.popen(f"sudo ip link set {self.module_name} down",'w',1)

    def send_q(self, id_list, brs_list, payload_list):
        for i in range(len(id_list)):
            os.popen(f"cansend {self.module_name} {id_list[i]}#{brs_list[i]}{payload_list[i]}", 'w',1)
            print(f"cansend {self.module_name} {id_list[i]}#{brs_list[i]}{payload_list[i]}", 'w',1)

    def dump_log(self, can_receiver):
        os.popen(f"candump {can_receiver} > CAN-Tester/can.log")
