import os

class CanModule():
    def __init__(self, txquelen = 1000, baudrate = 1000000, dbaudrate = 5000000):
        self.txquelen = txquelen
        self.baudrate = ""
        self.dbaudrate = ""
        self.frame_que = []
        self.module_name = ""
        self.can_status_var = False

    def set_can_status(self, status):
        self.can_status_var = status

    def get_can_status(self):
        return self.can_status_var

    #module name
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
        os.popen(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on", 'w', 128)
        print(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on")
        os.popen(f"sudo ifconfig {self.module_name} txqueuelen 65536", 'w', 128)
        print(f"sudo ifconfig {self.module_name} txqueuelen 65536")        
    
    def can_dump(self):
        os.popen(f"cat can.log")
        os.popen(f"candump {self.module_name} > ../logs/can.log", "w", 128)
        print("---")

    def interface_down(self):
        os.popen(f"sudo ip link set {self.module_name} down",'w', 128)

    def send_q(self, id_list, brs_list, payload_list):
        for i in range(len(id_list)):
            print(f"module name {type(self.module_name)}, id list {type(id_list)}, brs {type(brs_list)}, payload {type(payload_list)}")
            if payload_list[i] == "R":
                os.popen(f"cansend {self.module_name} {id_list[i]}#{payload_list[i]}", 'w', 128)
            else:
                os.popen(f"cansend {self.module_name} {id_list[i]}##{brs_list[i]}{payload_list[i]}", 'w', 128)
                print(f"cansend {self.module_name} {id_list[i]}##{brs_list[i]}{payload_list[i]}")

    def dump_log(self, can_receiver):
        os.popen(f"candump {can_receiver} > ../logs/can.log")

    def random_message(self, message):
        os.popen(f"cansend {self.module_name} {message}")

    def default_canup(self):
        os.popen(f"sudo ip link set can0 up type can bitrate 1000000  dbitrate 5000000 restart-ms 1000 berr-reporting on fd on", 'w')
        os.popen(f"sudo ip link set can1 up type can bitrate 1000000  dbitrate 5000000 restart-ms 1000 berr-reporting on fd on", 'w')
        os.popen(f"sudo ifconfig can0 txqueuelen 65536", 'w')
        os.popen(f"sudo ifconfig can1 txqueuelen 65536", 'w')

    def default_candump(self):
        os.popen(f"candump can1 > ../logs/can.log", 'w')

    def default_message_func(self):
        os.popen(f"cansend can0 123#1223", 'w')