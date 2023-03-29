from can_frame import CanFrame
from GUI import *
from can_module import CanModule
from tkinter import ttk
import os



if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

if __name__ == "__main__":
    root = Tk()
    splash = SplashScreen(root)
    for i in range(100):
        root.update()
        splash.progressbar.step(1)
        time.sleep(0.01)
    splash.destroy()
    root.mainloop()
    
    gui = CANGui("v.1.8.0")
    # MAJOR.MINOR.PATCH
    gui.build()
    gui.root.mainloop()