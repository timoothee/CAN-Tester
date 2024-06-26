import os
import time
import RPi.GPIO as GPIO

class CanModule():
    def __init__(self, txquelen = 1000, baudrate = 1000000, dbaudrate = 5000000, sample_point = 0.750, dsample_point = 0.750):
        self.txquelen = txquelen
        self.baudrate = ""
        self.dbaudrate = ""
        self.frame_que = []
        self.module_name = ""
        self.sample_point = sample_point
        self.dsample_point = ''
        self.can_status_var = False
        gpio = 15
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) 
        GPIO.setup(gpio,GPIO.OUT)
        GPIO.output(gpio,GPIO.LOW)
        self.rasp_path = str((os.popen("pwd", 'r', 128)).read()).strip().replace('/source', '/logs/')

    def set_rasp_path(self, path):
        self.rasp_path = path

    def get_rasp_path(self):
        return self.rasp_path

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
    
    #sample point
    def set_sample_point(self, sample_point):
        self.sample_point = sample_point
    
    def get_sample_point(self):
        response = os.popen(f"ip -d -s link show {self.module_name}", 'r', 128)
        response = response.read()
        for line in response.split('\n'):
            if 'sample-point' in line:
                return line.split()[-1]

    #dsample-point
    def set_dsample_point(self, dsample_point):
        if dsample_point == '':
            dsample_point = '0.750'
        print(type(dsample_point))
        self.dsample_point = dsample_point
        print("here", self.dsample_point)

    def get_dsample_point(self):
        response = os.popen(f"ip -d -s link show {self.module_name}", 'r', 128)
        response = response.read()
        for line in response.split('\n'):
            if 'dsample-point' in line:
                return line.split()[-1]

    
    def interface_up(self):
        os.popen(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on dsample-point {self.dsample_point}", 'w', 128)
        print(f"sudo ip link set {self.module_name} up type can bitrate {self.baudrate}  dbitrate {self.dbaudrate} restart-ms 1000 berr-reporting on fd on dsample-point {self.dsample_point}")
        os.popen(f"sudo ifconfig {self.module_name} txqueuelen 65536", 'w', 128)
        print(f"sudo ifconfig {self.module_name} txqueuelen 65536")        
    
    def can_dump(self):
        print("start")
        os.popen(f"cat {self.rasp_path}can.log")
        os.popen(f"candump {self.module_name} > {self.rasp_path}can.log", "w", 128)
        print("end")

    def interface_down(self):
        os.popen(f"sudo ip link set {self.module_name} down",'w', 128)

    def send_q(self, id_list, brs_list, payload_list, fd_list):
        for i in range(len(id_list)):
            print(f"module name {type(self.module_name)}, id list {type(id_list)}, brs {type(brs_list)}, payload {type(payload_list)}")
            if payload_list[i] == "R":
                GPIO.output(15,GPIO.HIGH)
                os.popen(f"cansend {self.module_name} {id_list[i]}#{payload_list[i]}", 'w', 128)
                GPIO.output(15,GPIO.LOW)
            if fd_list[i] == "0":
                GPIO.output(15,GPIO.HIGH)
                os.popen(f"cansend {self.module_name} {id_list[i]}#{payload_list[i]}", 'w', 128)
                GPIO.output(15,GPIO.LOW)
            else:
                GPIO.output(15,GPIO.HIGH)
                print(self.module_name)
                print(id_list[i])
                print(brs_list[i])
                print(payload_list[i])
                os.popen(f"cansend {self.module_name} {id_list[i]}##{brs_list[i]}{payload_list[i]}", 'w', 128)
                print(f"cansend {self.module_name} {id_list[i]}##{brs_list[i]}{payload_list[i]}")
                GPIO.output(15,GPIO.LOW)
        
    def default_led(self):
        pass
        #GPIO.output(15,GPIO.HIGH)

    def dump_log(self, can_receiver):
        os.popen(f"candump {can_receiver} > ../logs/can.log")

    def random_message(self, message):
        GPIO.output(15,GPIO.HIGH)
        os.popen(f"cansend {self.module_name} {message}")
        GPIO.output(15,GPIO.LOW)

    def default_canup(self):
        os.popen(f"sudo ip link set can0 up type can bitrate 1000000  dbitrate 5000000 restart-ms 1000 berr-reporting on fd on", 'w')
        os.popen(f"sudo ip link set can1 up type can bitrate 1000000  dbitrate 5000000 restart-ms 1000 berr-reporting on fd on", 'w')
        os.popen(f"sudo ifconfig can0 txqueuelen 65536", 'w')
        os.popen(f"sudo ifconfig can1 txqueuelen 65536", 'w')

    def default_candump(self):
        os.popen(f"candump can1 > ../logs/can.log", 'w')

    def default_message_func(self):
        os.popen(f"cansend can0 123#1223", 'w')