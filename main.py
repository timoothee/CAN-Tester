#import can_interface
from can_frame import CanFrame
#from can_interface import CANInterface
from can_interface1 import *
from can_module import CanModule
from tkinter import ttk

interface = CANInterface()


if __name__ == "__main__":
    interface.build()

    interface.root.mainloop()

    fdbox = interface.fd_box.get()
    extbox = interface.ext_box.get()
    frameid = interface.id_text.get()
    payloadsize = interface.payload_size_text.get()
    payload = interface.payload_text.get()

    x = CanFrame(frameid, extbox, fdbox, payloadsize, payload)