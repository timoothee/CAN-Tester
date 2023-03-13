from tkinter import *
import os
class CAN_gui_dev():

    def __init__(self):
        self.message = StringVar
        

    def build(self):
        self.message_label = Label(self.root_dev, text="Message")
        self.message_label.grid(row=0,column=0)

        self.message_entry = Entry(self.root_dev, textvariable=self.message)
        self.message_entry.grid(row=1,column=0)

        self.send_button = Button(self.root_dev, text= "Send", command=self.send_func)
        self.send_button.grid(row=0, column=1)


    def send_func(self):
        os.popen({str(self.message)}, "w")
       