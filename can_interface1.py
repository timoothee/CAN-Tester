from tkinter import *
from tkinter.ttk import Progressbar
import time
from tkinter import ttk


class CANInterface():

    def __init__(self):
        self.root = Tk("")
        self.root.title("BetterthanVector")
        self.root.iconbitmap("Raspberry.ico")
        self.root.geometry("600x700")

        self.fd_box = IntVar()
        self.ext_box = IntVar()
        self.id_text = StringVar()
        self.id_text.trace("w", self.callback)
        self.payload_size_entry = StringVar()
        self.payload_size_entry.trace("w", self.callback)
        self.payload_entry = StringVar()
        self.payload_entry.trace("w", self.callback)
        self.drop_down_menu_can = StringVar()
        self.drop_down_menu_can.set("Select")
        self.drop_down_id_baudrate_var = IntVar()
        self.drop_down_id_baudrate_var.set("Select")
        self.drop_down_data_baudrate_var = IntVar()
        self.drop_down_data_baudrate_var.set("Select")
        self.position = 0
        self.can_interface_list = ('CAN0', 'CAN1')
        self.baudrate_list = ('1M','2M','5M','8M')
        self.data_baudrate_list = ('1M','2M','5M','8M')



    def callback(self, *args):
        self.frame_uncompleted()

        if self.retVal == 0:
            self.add_to_q.config(state= "normal")
        else:
            self.add_to_q.config(state= "disabled")

        print("retvval", self.retVal)
        print(self.id_text.get())


    def build(self):
        
        self.can_frame1 = Frame(self.root)
        self.can_frame1.grid(row=0, column=0, sticky="nsew")

        self.can_frame2 = Frame(self.root)
        self.can_frame2.grid(row=1, column=0, sticky="nsew")

        self.can_frame3 = Frame(self.root)
        self.can_frame3.grid(row=2, column=0, sticky="nsew")

        self.can_frame4 = Frame(self.root)
        self.can_frame4.grid(row=3, column=0, sticky="nsew")

        self.can_frame5= Frame(self.root)
        self.can_frame5.grid(row=5, column=0, sticky="nsew")

        self.can_frame6 = Frame(self.root)
        self.can_frame6.grid(row=6, column=0, sticky="nsew")

        self.listbox1 = Listbox(self.can_frame3, yscrollcommand = 1, width = 60, selectmode=EXTENDED)
        self.listbox2 = Listbox(self.can_frame5, yscrollcommand = 1, width = 60, selectmode =EXTENDED)

        self.can_interface_Label = Label(self.can_frame1, text = "Can interface")
        self.can_interface_Label.grid(row=0, column=0, padx=20, pady=(20,0))

        self.drop_down_menu = OptionMenu(self.can_frame1, self.drop_down_menu_can, *self.can_interface_list)
        self.drop_down_menu.config(width=5)
        self.drop_down_menu.grid(row = 1, column = 0)


        self.can_interface_Label = Label(self.can_frame1, text = "Id Baudrate")
        self.can_interface_Label.grid(row=0, column=1, padx=20, pady=(20,0))

        self.drop_down_id_baudrate = OptionMenu(self.can_frame1,  self.drop_down_id_baudrate_var, *self.baudrate_list)
        self.drop_down_id_baudrate.config(width=5, state="disabled")
        self.drop_down_id_baudrate.grid(row = 1, column=1, padx= 20)


        self.can_interface_Label = Label(self.can_frame1, text = "Data Baudrate")
        self.can_interface_Label.grid(row=0, column=2, padx=20, pady=(20,0))

        self.drop_down_data_baudrate = OptionMenu(self.can_frame1, self.drop_down_data_baudrate_var, *self.data_baudrate_list)
        self.drop_down_data_baudrate.config(width=5, state="disabled")
        self.drop_down_data_baudrate.grid(row = 1, column=2, padx= 20 )

        
        self.fd_Label = Label(self.can_frame2, text="Fd")
        self.fd_Label.grid(row= 0, column =0, padx=(40,0), pady=(50,0))

        self.fd_CkBt = Checkbutton(self.can_frame2, variable=self.fd_box, command= lambda: self.fd_box_checked())
        self.fd_CkBt.grid(row = 1, column=0, padx=(40,0), pady=(2,0))

        self.ext_flag_Label = Label(self.can_frame2, text="Ext")
        self.ext_flag_Label.grid(row =0 ,column=2, pady=(50,0))

        self.ext_flag_CkBt = Checkbutton(self.can_frame2, variable=self.ext_box, command= lambda: self.extended_box_checked())
        self.ext_flag_CkBt.grid(row=1, column=2, padx= 10, pady=(2,0))


        self.frame_id_Label = Label(self.can_frame2, text="Id (0x)")
        self.frame_id_Label.grid(row = 0, column=3, pady=(50,0))

        self.frame_id_entry = Entry(self.can_frame2, textvariable=self.id_text, width= 5)
        self.frame_id_entry.grid(row = 1, column=3, padx=(5,0), pady=(2,0))


        self.payload_size_Label = Label(self.can_frame2, text="Payload\nSize", state="disabled")
        self.payload_size_Label.grid(row = 0, column=4, pady=(50,0))

        self.payload_size_Entry = Entry(self.can_frame2, textvariable=self.payload_size_entry, width= 5, state="disabled")
        self.payload_size_Entry.config(state="disabled", highlightbackground= "grey", highlightthickness=0)
        self.payload_size_Entry.grid(row = 1, column=4, pady=(2,0))


        self.payload_Label = Label(self.can_frame2, text="Payload")
        self.payload_Label.grid(row = 0, column=5, pady=(50,0))

        self.payload_Entry = Entry(self.can_frame2, textvariable=self.payload_entry)
        self.payload_Entry.grid(row = 1, column=5, pady=(2,0))

        self.send_button = Button(self.can_frame1, text="Send", command=self.progress_bar, state="disabled")
        self.send_button.grid(row = 1, column=3, padx=(110,0))

        #self.pb = Progressbar(self.root, orient='horizontal', mode='determinate', length=63)
        #self.pb.grid(row = 2, column=7)

        self.add_to_q = Button(self.can_frame2, text="Add to q", command=self.clear_text, state="disabled", fg='red')
        self.add_to_q.grid(row = 1, column=6)

        self.listbox1.grid(row=0, column=0, padx=20, pady=(20,10))

        self.import_button = Button(self.can_frame4, text="Import", command = self.import_messagges)
        self.import_button.grid(row=0, column=0, padx=(20,0))

        self.save_button = Button(self.can_frame4, text="Save", command = self.import_messagges)
        self.save_button.grid(row=0, column=1, padx=10)

        self.clear_button = Button(self.can_frame4, text="Clear", command = lambda: self.delete_function(self.listbox1))
        self.clear_button.grid(row=0, column=2)

        self.listbox2.grid(row=0, column=0, padx=20, pady=(40,10))

        self.save_button = Button(self.can_frame6, text="Save", command = self.import_messagges)
        self.save_button.grid(row=0, column=1, padx=(20,10))

        self.clear_button1 = Button(self.can_frame6, text="Clear", command = lambda: self.delete_function(self.listbox2))
        self.clear_button1.grid(row=0, column=2)

        self.Error_label = Label(self.root, text = "")
        self.Error_label.grid(row = 1, column= 3)
        

    def delete_function(self, listbox):
        listbox.delete(ANCHOR)


    def import_messagges(self):
        pass

    def frame_uncompleted(self):
        self.retVal = 0
        if len(self.frame_id_entry.get()) < 4 or self.frame_id_entry.get()[0] != "0" or self.frame_id_entry.get()[1] != "x":
            self.retVal = 1
        if len(self.payload_size_entry.get()) < 1:
            self.retVal = 1
        if len(self.payload_Entry.get()) < 3 or self.payload_Entry.get()[2] != ".":
            self.retVal = 1

    def refresh_time(self):
        self.t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", self.t)

    def get_frame_data(self):
        self.string = self.current_time + "  " + self.frame_id_entry.get() + self.payload_entry.get()
        print(self.string)
        self.position += 1
    
    def fd_box_checked(self):
        self.fd_box_checked_retVal = False
        if self.fd_box.get() == 1:
            self.drop_down_id_baudrate.config(state="normal")
            self.drop_down_data_baudrate.config(state="normal")
            self.fd_box_checked_retVal = True
        else:
            self.drop_down_id_baudrate.config(state="disabled")
            self.drop_down_id_baudrate_var.set("Select")
            self.drop_down_data_baudrate.config(state="disabled")
            self.drop_down_data_baudrate_var.set("Select")
            

    def extended_box_checked(self):
        self.extended_box_checked_retVal = False
        if self.ext_box.get() == 1:
            self.payload_size_Label.config(state="normal")
            self.payload_size_Entry.config(state="normal")
            self.extended_box_checked_retVal = True
        else:
            self.payload_size_Entry.delete(0, 'end')
            self.payload_size_Label.config(state="disabled")
            self.payload_size_Entry.config(state="disabled", highlightbackground= "grey", borderwidth=1)


    def check_all_fields(self):
        self.box_retVal = False
        if self.ext_box.get() == 1:
            if int(self.frame_id_entry.get(), 16) < 2047:
                self.box_retVal = True
            if len(self.frame_id_entry.get()) < 6:
                self.box_retVal = True
        else:
            if len(self.frame_id_entry.get()) > 4:
                self.box_retVal = True
 

    def clear_text(self):
        self.check_all_fields()
        if self.box_retVal:
            self.Error_label.config(text="Error", fg='red')
        else:
            self.refresh_time()
            self.Error_label.config(text="")
            self.get_frame_data()
            self.frame_id_entry.delete(0, 'end')
            self.payload_size_Entry.delete(0, 'end')
            self.payload_Entry.delete(0, 'end')
            self.fd_box.set(0)
            self.ext_box.set(0)
            self.listbox1.insert(self.position, self.string)


    def progress_bar(self):
        for i in range(100):
            self.root.update_idletasks()
            self.pb['value'] += 1
            time.sleep(0.001)
        time.sleep(2)
        self.pb['value'] = 0
    