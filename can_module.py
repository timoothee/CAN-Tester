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
        os.popen(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on", 'w')
        print(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on")
        os.popen(f"sudo ifconfig {self.module_name} txqueuelen 65536")
        print(f"sudo ifconfig {self.module_name} txqueuelen 65536")        
    def can_dump(self):
        os.popen(f"candump {self.module_name} > can.log", "w")
        print("---")

    def interface_down(self):
        os.popen(f"sudo ip link set {self.module_name} down",'w')

    def send_q(self, id_list, brs_list, payload_list):
        itemi = ''
        for i in range(len(id_list)):
            '''
            self.message_string = "cansend " + self.module_name + id_list[i] + "#" + brs_list[i] + payload_list[i]
            self.message_string = str(self.message_string, encoding='utf-8')
            self.message_string = self.message_string.strip()
            self.message_string = self.message_string.replace(b'\x00'.decode(),'')
            '''
            itemi = str(b'self.module_name', encoding='utf-8')
            itemi= self.module_name.strip()
            itemi = self.module_name.replace(b'\x00'.decode(), '')   
            os.popen(f"cansend {self.module_name} {id_list[i]}#{brs_list[i]}{payload_list[i]}", 'w')
            print(f"cansend {self.module_name} {id_list[i]}#{brs_list[i]}{payload_list[i]}")

    def dump_log(self, can_receiver):
        os.popen(f"candump {can_receiver} > CAN-Tester/can.log")
