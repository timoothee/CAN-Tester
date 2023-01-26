import CanFrame
from gui import *

fdbox = fd_box.get()
extbox = ext_box.get()
frameid = id_text.get()
payloadsize = payload_size_text.get()
payload = payload_text.get()

x = CanFrame.Can(frameid, extbox, fdbox, payloadsize, payload)
