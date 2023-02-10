from tkinter import *
from tkinter.ttk import Progressbar
import time

retVal = False

class CANInterface():

    def __init__(self):
        self.root = Tk()
        self.fd_box = IntVar()
        self.ext_box = IntVar()
        self.id_text = IntVar()
        self.drop_down = IntVar(self.root)
        self.drop_down_mess_number1 = IntVar(self.root)
        self.drop_down.set("Select an option")
        self.drop_down_mess_number1.set("3")
        self.payload_size_text = StringVar()
        self.payload_text = StringVar()
        self.message_options = ('1','2','3','4','5','6','7','8','9','10')


    def whole_picture(self, ):
        print("i m in")

        print("1", type(self.drop_down_mess_number1))

        for i in range(self.drop_down_mess_number1.get()):
            print(i, "time")


    def callback_message_number(self, selection):
        self.whole_picture()
        print(selection)
        #self.drop_down_mess_number1 = selection
        print("2", type(self.drop_down_mess_number1))


    def build(self):
        self.root.geometry("500x500")
        self.drop_down_menu = OptionMenu(self.root, self.drop_down, "MAX232", "MIN232")
        self.drop_down_menu.place(x = 50, y = 30)

        self.drop_down_mess_number = OptionMenu(self.root, self.drop_down_mess_number1, *self.message_options, command = self.callback_message_number)
        self.drop_down_mess_number.place(x = 50, y = 60)

        self.fd_Label = Label(self.root, text = "Fd")
        self.fd_Label.place(x = 50, y = 100)

        self.fd_CkBt = Checkbutton(self.root, variable = self.fd_box)
        self.fd_CkBt.place(x = 50, y = 120)


        self.ext_flag_Label = Label(self.root, text="Ext")
        self.ext_flag_Label.place(x = 100, y = 100)

        self.ext_flag_CkBt = Checkbutton(self.root, variable = self.ext_box)
        self.ext_flag_CkBt.place(x = 100, y = 120)


        self.frame_id_Label = Label(self.root, text = "Id")
        self.frame_id_Label.place(x=150 , y=100)

        self.frame_id_entry = Entry(self.root, textvariable = self.id_text)
        self.frame_id_entry.place(x=150, y=120, width= 45)

        self.payload_size_Label = Label(self.root, text = "Payload\nSize")
        self.payload_size_Label.place(x = 200, y = 82)

        self.payload_size_Entry = Entry(self.root, textvariable = self.payload_size_text)
        self.payload_size_Entry.place(x=200, y=120, width= 60)

        self.payload_Label = Label(self.root, text = "Payload\nSize")
        self.payload_Label.place(x = 270, y = 100)

        self.payload_Entry = Entry(self.root, textvariable = self.payload_text)
        self.payload_Entry.place(x=270, y=120, width= 40)

        self.send_button = Button(self.root, text = "Send", command = self.Show)
        self.send_button.place(x = 450, y = 30, anchor = 'ne')

        self.pb = Progressbar(self.root,orient='horizontal',mode='determinate',length=63)
        self.pb.place(x = 385, y = 60)
        

    def send(self):
        pass


    def Show(self):
        for i in range(100):
            self.root.update_idletasks()
            self.pb['value'] += 1
            time.sleep(0.001)

        
