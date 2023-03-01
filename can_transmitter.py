import os
class CanTrasnmitter():
    def __init__(self):
        pass

    def interface_up(self, can_interface, can_baudrate, can_dbaudrate):
        os.popen(f"sudo ip link set {can_interface} up type can bitrate {can_baudrate}  dbitrate {can_dbaudrate} restart-ms 1000 berr-reporting on fd on", 'w',1)
        print(f"sudo ip link set {can_interface} up type can bitrate {can_baudrate}  dbitrate {can_dbaudrate} restart-ms 1000 berr-reporting on fd on")


    def interface_down(self, can_interface):
        os.popen(f"sudo ip link set {can_interface} down",'w',1)

    def send_q(self, id_list, brs_list, payload_list, can_sender):
        for i in range(len(id_list)):
            os.popen(f"cansend {can_sender} {id_list[i]}##{brs_list[i]}.{payload_list[i]}", 'w',1)