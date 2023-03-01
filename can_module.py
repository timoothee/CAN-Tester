import os

class CanModule():
    def __init__(self, txquelen = 1000, baudrate = 1000000, dbaudrate = 8000000):
        self.can_send_module_name = ""
        self.can_receive_module_name = ""
        self.txquelen = txquelen
        self.baudrate = ""
        self.dbaudrate = ""
        self.frame_que = []

    #can_sender
    def set_can_sender_module_name(self, name):
        self.can_send_module_name = name

    def get_can_sender_module_name(self):
        return self.can_send_module_name

    #can_receiver
    def set_can_receiver_module_name(self, name):
        self.can_receive_module_name = name

    def get_can_receiver_module_name(self):
        return self.can_receive_module_name

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