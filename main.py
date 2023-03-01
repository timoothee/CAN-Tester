from can_frame import CanFrame
from GUI import *
from can_module import CanModule
from tkinter import ttk
import os

gui = CANGui("v.1.3.5")
# MAJOR.MINOR.PATCH

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

if __name__ == "__main__":
    gui.build()
    gui.root.mainloop()

    brsbox = gui.brs_box.get()
    extbox = gui.ext_box.get()
    frameid = gui.id_text.get()
    #payloadsize = gui.payload_size_entry.get()
    payload = gui.payload_entry.get()

    x = CanFrame(frameid, extbox, brsbox, payload)