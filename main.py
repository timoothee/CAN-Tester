from can_frame import CanFrame
from can_interface import *
from can_module import CanModule
from tkinter import ttk
import os

interface = CANInterface("v.1.2.5")
# MAJOR.MINOR.PATCH

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

if __name__ == "__main__":
    interface.build()
    interface.root.mainloop()

    fdbox = interface.fd_box.get()
    extbox = interface.ext_box.get()
    frameid = interface.id_text.get()
    payloadsize = interface.payload_size_entry.get()
    payload = interface.payload_entry.get()

    x = CanFrame(frameid, extbox, fdbox, payloadsize, payload)