from can_frame import CanFrame
from GUI import *
from can_module import CanModule
from tkinter import ttk
import os
from splash import SplashScreen


if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

if __name__ == "__main__":
    gui = CANGui("v.1.8.0")
    # MAJOR.MINOR.PATCH
    gui.build()
    gui.parent.mainloop()

    