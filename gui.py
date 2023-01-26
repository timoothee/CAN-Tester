from tkinter import *
from tkinter.ttk import Progressbar
import time

root = Tk()

fd_box = IntVar()
ext_box = IntVar()
id_text = IntVar()
drop_down = StringVar(root)
drop_down.set("Select an option")
payload_size_text = StringVar()
payload_text = StringVar()

root.geometry("500x500")

def Show():
    for i in range(100):
        root.update_idletasks()
        pb['value'] += 1
        time.sleep(0.001)
        
    pass
    

drop_down_menu = OptionMenu(root, drop_down, "MAX232", "MIN232")
drop_down_menu.place(x = 50, y = 30)

fd_Label = Label(root, text = "Fd")
fd_Label.place(x = 50, y = 100)

fd_CkBt = Checkbutton(root, variable = fd_box)
fd_CkBt.place(x = 50, y = 120)


ext_flag_Label = Label(root, text="Ext")
ext_flag_Label.place(x = 100, y = 100)

ext_flag_CkBt = Checkbutton(root, variable = ext_box)
ext_flag_CkBt.place(x = 100, y = 120)


frame_id_Label = Label(root, text = "Id")
frame_id_Label.place(x=150 , y=100)

frame_id_entry = Entry(root, textvariable = id_text)
frame_id_entry.place(x=150, y=120, width= 45)

payload_size_Label = Label(root, text = "Payload\nSize")
payload_size_Label.place(x = 200, y = 82)

payload_size_Entry = Entry(root, textvariable = payload_size_text)
payload_size_Entry.place(x=200, y=120, width= 60)

payload_Label = Label(root, text = "Payload\nSize")
payload_Label.place(x = 270, y = 100)

payload_Entry = Entry(root, textvariable = payload_text)
payload_Entry.place(x=270, y=120, width= 40)

send_button = Button(root, text = "Send", command = Show)
send_button.place(x = 450, y = 30, anchor = 'ne')

pb = Progressbar(root,orient='horizontal',mode='determinate',length=63)
pb.place(x = 385, y = 60)


root.mainloop()
