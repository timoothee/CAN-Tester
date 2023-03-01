from tkinter import *
from tkinter.ttk import Progressbar
import time
from tkinter import ttk
import ast
import os
from tkinter import messagebox
import sys
#from tkmacosx import Button
import can_module as CAN_module
import can_frame as CAN_frame
import can_transmitter as CAN_transmitter


class CANGui():

    def __init__(self, gui_revision: str):
        self.gui_revision = gui_revision
        self.root = Tk()
        self.root.title(f"CanInterfaceGUI {self.gui_revision}")
        #self.root.iconbitmap("./Raspberry icon/Raspberry.ico")
        self.root.geometry("600x800")

        self.brs_box = IntVar()
        self.ext_box = IntVar()
        self.id_text = StringVar()
        self.RTR_box = IntVar()
        self.payload_size_entry = IntVar()
        self.payload_size_entry.set("")
        self.payload_entry = StringVar()
        self.payload_entry.set("")
        self.drop_down_menu_can = StringVar()
        self.drop_down_menu_can.set("Select")
        self.interface_var = StringVar()
        self.interface_var.set('Select')
        self.sender_var = StringVar()
        self.sender_var.set('Select')
        self.can_sender_var = StringVar()
        self.can_sender_var.set('Select')
        self.can_sender_var.trace("w", self.can_frame_option_changed)
        self.can_receiver_var = StringVar()
        self.can_receiver_var.set('Select')
        self.can_receiver_var.trace("w", self.can_frame_option_changed_1)
        self.receiver_var = StringVar()
        self.receiver_var.set('Select')
        self.interface_var.trace("w", self.can_frame_option_changed)
        self.drop_down_id_baudrate_var = StringVar()
        self.drop_down_id_baudrate_var.set("Select")
        self.drop_down_id_baudrate_var.trace("w", self.id_baudrate_option_changed)
        self.drop_down_data_baudrate_var = StringVar()
        self.drop_down_data_baudrate_var.set("Select")
        self.drop_down_data_baudrate_var.trace("w", self.data_baudrate_option_changed)
        self.position = 0
        self.can_send_module_optionmenu = None
        self.can_receive_module_optionmenu = None
        self.can_module_optionmenu = ("Sender", "Receiver")
        self.can_send_module_optionmenu = ("CAN0", "CAN1")
        self.can_receive_module_optionmenu = ("CAN0", "CAN1")
        self.can_interface_list = ('Sender', 'Receiver')
        self.baudrate_list = ('100K','200K','400K','500K','1M','2M','5M','8M')
        self.data_baudrate_list = ('100K','200K','400K','500K','1M','2M','3M','4M','5M','6M','7M','8M')
        self.baudrate_dict = {'100K':100000,'200K':200000,'400K':400000,'500K':500000,"1M":1000000,"2M":2000000,'3M':3000000,'4M':4000000,"5M":5000000,"6M":6000000,"7M":7000000,"8M":8000000}
        self.can_dict = {'CAN0':"can0", 'CAN1':"can1", 'CAN2':"can2"}        
        self.can_frame_changed = False
        self.can_down_var = True
        self.module = CAN_module.CanModule()
        self.frame = CAN_frame.CanFrame()
        self.transmitter = CAN_transmitter.CanTrasnmitter()


    def build(self):
        self.can_frame1 = Frame(self.root)
        self.can_frame1.grid(row=0, column=0, sticky="nsew")

        self.can_frame2 = Frame(self.root)
        self.can_frame2.grid(row=1, column=0, pady=15, sticky="nsew")

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

        self.can_interface_Label = Label(self.can_frame1, text = "Can Sender")
        self.can_interface_Label.grid(row=0, column=0, padx=20, pady=(20,0))

        self.drop_down_menu = OptionMenu(self.can_frame1, self.can_sender_var, *self.can_send_module_optionmenu)
        self.drop_down_menu.config(width=5)
        self.drop_down_menu.grid(row = 1, column = 0)

        self.can_interface_Label_1 = Label(self.can_frame1, text = "Can Receiver")
        self.can_interface_Label_1.grid(row=2, column=0)

        self.drop_down_menu_1 = OptionMenu(self.can_frame1, self.can_receiver_var, *self.can_receive_module_optionmenu)
        self.drop_down_menu_1.config(width=5)
        self.drop_down_menu_1.grid(row = 3, column = 0)

        self.id_baudrate_Label = Label(self.can_frame1, text = "Id Baudrate")
        self.id_baudrate_Label.grid(row=0, column=1, pady=(20,0))

        self.drop_down_id_baudrate = OptionMenu(self.can_frame1,  self.drop_down_id_baudrate_var, *self.baudrate_list)
        self.drop_down_id_baudrate.config(width=5)
        self.drop_down_id_baudrate.grid(row = 1, column=1)

        self.data_baudrate_Label = Label(self.can_frame1, text = "Data Baudrate")
        self.data_baudrate_Label.grid(row=0, column=2, pady=(20,0))

        self.drop_down_data_baudrate = OptionMenu(self.can_frame1, self.drop_down_data_baudrate_var, *self.data_baudrate_list)
        self.drop_down_data_baudrate.config(width=5)
        self.drop_down_data_baudrate.grid(row = 1, column=2)

        self.status_label = Label(self.can_frame1, text="STATUS")
        self.status_label.grid(row=0, column=3, padx=(150,0), pady=(20,0))

        self.default_status_label = Label(self.can_frame1, text="DOWN", fg='red')
        self.default_status_label.grid(row=0, column=4, pady=(20,0))
        
        self.up_down_button = Button(self.can_frame1, text="UP",fg="green", command=self.up_down_button_command, width=3, state="disabled")
        self.up_down_button.grid(row=1, column=4, sticky='w')

        self.RTR_Label = Label(self.can_frame2, text="RTR")
        self.RTR_Label.grid(row= 0, column =0, padx=(20,0))

        self.RTR_CkBtn = Checkbutton(self.can_frame2, variable=self.RTR_box)
        self.RTR_CkBtn.grid(row = 1, column=0, padx=(20,0))

        self.brs_Label = Label(self.can_frame2, text="Brs")
        self.brs_Label.grid(row= 0, column =1)

        self.brs_CkBt = Checkbutton(self.can_frame2, variable=self.brs_box, command= lambda: self.brs_box_checked())
        self.brs_CkBt.grid(row = 1, column=1)

        self.ext_flag_Label = Label(self.can_frame2, text="Ext")
        self.ext_flag_Label.grid(row =0 ,column=2)

        self.ext_flag_CkBt = Checkbutton(self.can_frame2, variable=self.ext_box)
        self.ext_flag_CkBt.grid(row=1, column=2)

        self.frame_id_Label = Label(self.can_frame2, text="Id (0x)")
        self.frame_id_Label.grid(row = 0, column=3, padx=(5,0), sticky='w')
        self.default_label_color = self.frame_id_Label.cget('fg')

        self.frame_id_entry = Entry(self.can_frame2, textvariable=self.id_text, width= 10)
        self.frame_id_entry.grid(row = 1, column=3, padx=(5,0))
        self.default_entry_color = self.frame_id_entry.cget('fg')

        self.payload_size_Label = Label(self.can_frame2, text="Payload\nSize", state="disabled")
        self.payload_size_Label.grid(row = 0, column=4)

        self.payload_size_Entry = Entry(self.can_frame2, textvariable=self.payload_size_entry, width= 5, state="disabled")
        self.payload_size_Entry.config(state="disabled", highlightbackground= "grey", highlightthickness=0)
        self.payload_size_Entry.grid(row = 1, column=4)


        self.payload_Label = Label(self.can_frame2, text="Payload")
        self.payload_Label.grid(row = 0, column=5, sticky='w')

        self.payload_Entry = Entry(self.can_frame2, textvariable=self.payload_entry)
        self.payload_Entry.grid(row = 1, column=5)

        #self.pb = Progressbar(self.root, orient='horizontal', mode='determinate', length=63)
        #self.pb.grid(row = 2, column=7)

        self.add_to_q = Button(self.can_frame2, text="Add to que", command= self.add_to_Q)
        self.add_to_q.grid(row = 1, column=6, padx=5)

        self.listbox1.grid(row=1, column=0, padx=20)

        self.que_listbox_label = Label(self.can_frame3, text = "Message list")
        self.que_listbox_label.grid(row=0, column=0, sticky='w', padx=20)
        self.que_listbox_label.config(font=('Helvetica bold', 13))

        self.can_bus_listbox_label = Label(self.can_frame5, text="CAN BUS")
        self.can_bus_listbox_label.grid(row=0, column=0, sticky='w',padx=20 ,pady=(15,0))
        self.can_bus_listbox_label.config(font=('Helvetica bold', 13))

        self.error_listbox_label = Label(self.can_frame6, text='Error list')
        self.error_listbox_label.grid(row=0, column=2, sticky='w', padx= 125,pady=(10,0))
        self.error_listbox_label.config(font=('Helvetica bold', 13))

        self.import_button = Button(self.can_frame4, text="Import", command = self.import_messagges)
        self.import_button.grid(row=0, column=0, padx=(20,0))

        self.save_button_input = Button(self.can_frame4, text="Save", command = self.save_messages_sent)
        self.save_button_input.grid(row=0, column=1, padx=10)

        self.clear_button_input = Button(self.can_frame4, text="Clear", command = lambda: self.delete_function(self.listbox1))
        self.clear_button_input.grid(row=0, column=2)

        self.send_button = Button(self.can_frame4, text="Send que", command=self.send_que, state="normal")
        self.send_button.grid(row = 0, column=5, padx=60, sticky='e')

        self.listbox2.grid(row=1, column=0, padx=20, pady=(5,10))

        self.save_button_output = Button(self.can_frame6, text="Save", command=lambda:self.save_messages_received())
        self.save_button_output.grid(row=0, column=0, padx=(20,10), sticky='n')

        self.clear_button_output = Button(self.can_frame6, text="Clear", command = lambda: self.delete_function(self.listbox2))
        self.clear_button_output.grid(row=0, column=1, sticky='n')

        self.Error_label = Label(self.can_frame2, text = "")
        self.Error_label.grid(row = 0, column= 5)

        self.Edit_button = Button(self.can_frame4, text="Edit", command= self.edit_button)
        self.Edit_button.grid(row=0, column=3, padx=(30,10))

        self.ok_button = Button(self.can_frame4, text= "OK", command= self.ok_command)
        self.ok_button.grid(row=0, column=4)

        self.error_listbox =Listbox(self.can_frame6, width = 30,height=4, selectmode=EXTENDED)
        self.error_listbox.grid(row=1, column= 2, padx=(127,0), pady=5)


    def up_down_button_command(self):
        if self.can_down_var:
            self.default_status_label.config(fg='green',text='UP')
            self.up_down_button.config(fg="red", text="DOWN")
            self.backend_module()
            self.can_down_var = False
        else:
            self.default_status_label.config(fg='red',text='DOWN')
            self.up_down_button.config(fg="green", text= "UP")
            self.backend_module()
            self.can_down_var = True

    def id_baudrate_option_changed(self, *args):
        self.id_baudrate_changed = True
        self.btn_up_down_active()

    def data_baudrate_option_changed(self, *args):
        self.data_baudrate_changed = True
        self.btn_up_down_active()

    def can_frame_option_changed(self, *args):
        self.can_frame_changed = True
        self.btn_up_down_active()

    def can_frame_option_changed_1(self, *args):
        self.can_frame_changed_1 = True
        self.btn_up_down_active()
        
    def delete_function(self, listbox):
        listbox.delete(ANCHOR)

    def ok_command(self):
        self.check_all_fields()
        if self.check_all_fields_retVal:
            self.fields_uncompleted_error()
            self.fields_completed_wrong_error()
        else:
            self.refresh_time()
            self.get_frame_data()
            
            self.listbox1.delete(self.our_item)
            self.listbox1.insert(self.our_item, self.string_max)
            self.listbox1.itemconfig(self.our_item, {'fg': 'green'})
            self.initial_interface_state()
        
    def edit_button(self):
        if self.listbox1.size() != 0:
            if len(self.listbox1.curselection()) != 0:
                self.initial_interface_state()
                self.our_item = self.listbox1.curselection()
                self.ok_button.config(state="normal")
                self.index_element = 0
                self.value = self.listbox1.get(self.listbox1.curselection())[10:]
                for element in self.value:
                    if element == "#":
                        if self.value[self.value.index(element)+1] == "#":
                            self.index_element += 1
                        break
                    self.index_element += 1
                    
                self.frame_id_entry.insert(0,self.value[0:self.index_element])
                self.payload_Entry.insert(0, self.value[self.index_element+1:])

                try:
                    if int(self.frame_id_entry.get(), 16) > 2047:
                        self.ext_flag_CkBt.select()
                except:
                    print("Not hexadecimal")

            else:
                messagebox.showerror("Status", "Select a message")
                
        else:
            messagebox.showerror("Status", "Listbox empty")


    def import_messagges(self):
        import tkinter.filedialog as fd
        self.ask_textfile_tk = Tk()
        self.ask_textfile_tk.withdraw()

        self.currdir = os.getcwd()
        self.path = fd.askopenfilename(parent= self.ask_textfile_tk, initialdir= self.currdir, title= "Please select a file")
        if not self.path:
            pass
        else:
            self.textfile = os.path.join(r"", self.path)
            with open(self.textfile) as f:
                self.lines = f.readlines()
            print(self.lines)

            self.refresh_time()
            
            for item in self.lines:
                self.string_import = self.current_time + "  " + item
                self.listbox1.insert(0, self.string_import)


    def btn_up_down_active(self, *args):
        try:
            if self.can_frame_changed == True and self.id_baudrate_changed == True and self.data_baudrate_changed == True and self.can_frame_changed_1 == True:
                self.up_down_button.config(state="normal")
        except:
            pass

    def check_all_fields_completed(self):
        self.check_all_fields_completed_retVal = False
        self.id_entry_error = False
        self.payload_size_error = False
        self.payload_entry_error = False
        if len(self.frame_id_entry.get()) != 0:
            pass
        else:
            self.id_entry_error = True
            self.check_all_fields_completed_retVal = True

        if len(self.payload_Entry.get()) != 0:
            pass
        else:
            self.payload_entry_error = True
            self.check_all_fields_completed_retVal = True

        if self.brs_box.get() == 1:
            if len(self.payload_size_Entry.get()) != 0:
                pass
            else:
                self.payload_size_error = True
                self.check_all_fields_completed_retVal = True

    def check_all_fields(self):
        self.check_all_fields_retVal = False
        if self.check_all_fields_completed_retVal:
            pass
        else:
            if self.ext_box.get() == 1:
                if int(self.frame_id_entry.get(), 16) < 2047:
                    self.id_entry_error = True
                    self.check_all_fields_retVal = True
            else:
                if int(self.frame_id_entry.get(), 16) > 2047 and self.brs_box.get() != 1:
                    self.id_entry_error = True
                    self.check_all_fields_retVal = True

            if self.brs_box.get() == 1:
                if int(self.frame_id_entry.get(), 16) < 2047:
                    self.id_entry_error = True
                    self.check_all_fields_retVal = True
                if self.payload_size_entry.get()*2 != len(str(self.payload_entry.get())):
                    self.payload_size_error = True
                    self.payload_entry_error = True
                    self.check_all_fields_retVal = True

    def fields_uncompleted_error(self):
        self.error_listbox.delete(0,END)
        self.frame_id_Label.config(fg=self.default_label_color)
        self.payload_size_Label.config(fg=self.default_label_color)
        self.payload_Label.config(fg=self.default_label_color)
        if self.check_all_fields_completed_retVal:
            if self.id_entry_error == True:
                self.frame_id_Label.config(fg='red')
                self.error_listbox.insert(END,"Error: Id uncompleted")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
            if self.payload_size_error == True:
                self.payload_size_Label.config(fg='red')
                self.error_listbox.insert(END,"Error: Payload size uncompleted")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
            if self.payload_entry_error == True:
                self.payload_Label.config(fg='red')
                self.error_listbox.insert(END,"Error: Payload uncompleted")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
    
    def fields_completed_wrong_error(self):
        if self.check_all_fields_retVal == True:
            self.error_listbox.delete(0,END)
            self.frame_id_entry.config(fg=self.default_entry_color)
            self.payload_size_Entry.config(fg=self.default_entry_color)
            self.payload_Entry.config(fg=self.default_entry_color)
            if self.id_entry_error == True:
                if self.ext_box.get() == 1:
                    self.error_listbox.insert(END,"Error: Ext selected, Id not ext")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.frame_id_entry.config(fg= 'red')
                if self.ext_box.get() == 0 and self.brs_box.get() == 0:
                    self.error_listbox.insert(END,"Error: Id ext")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.frame_id_entry.config(fg= 'red')
                if self.brs_box.get() == 1:
                    self.error_listbox.insert(END,"Error: Fd selected, Id not ext")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.frame_id_entry.config(fg= 'red')
            if self.payload_size_error == True or self.payload_entry_error == True:
                self.error_listbox.insert(END,"Error: Payload not equal to payload size")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
                self.payload_size_Entry.config(fg= 'red')
                self.payload_Entry.config(fg= 'red')
                

    def refresh_time(self):
        self.t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", self.t)

    def get_frame_data(self):
            self.string_max = self.current_time + "  " + str(self.frame_id_entry.get()) + "##" + str(self.brs_box.get()) + "." + str(self.payload_entry.get())
            self.position += 1


    def brs_box_checked(self):
        self.brs_box_checked_retVal = False
        self.id_baudrate_changed = False
        self.data_baudrate_changed = False

        if self.brs_box.get() == 1:
            self.payload_size_Label.config(state="normal")
            self.payload_size_Entry.config(state="normal")
            self.brs_box_checked_retVal = True
        else:
            self.payload_size_Entry.delete(0, 'end')
            self.payload_size_Label.config(state="disabled")
            self.payload_size_Entry.config(state="disabled")
    
    def save_messages_sent(self):
        with open("Messages_sent.txt","w") as f:
            for i in self.listbox1.get(0,END):
                f.write(i+"\n")

    def save_messages_received(self):
        with open("Messages_received.txt","w") as f:
            for i in self.listbox1.get(0,END):
                f.write(i+"\n")

            else:
                if int(self.frame_id_entry.get(), 16) > 2047:
                    self.id_entry_error = True
                    self.check_all_fields_retVal = True

        
    def initial_interface_state(self):
        self.Error_label.config(text="")
        self.brs_box.set(0)
        self.ext_box.set(0)   
        self.frame_id_entry.delete(0, 'end')
        self.payload_size_Entry.delete(0, 'end')
        self.payload_size_Label.config(state="disabled")
        self.payload_size_Entry.config(state="disabled", highlightbackground= "grey", borderwidth=1)
        self.payload_Entry.delete(0, 'end')
        self.error_listbox.delete(0,END)
        self.frame_id_Label.config(fg=self.default_label_color)
        self.payload_size_Label.config(fg=self.default_label_color)
        self.payload_Label.config(fg=self.default_label_color)
        self.frame_id_entry.config(fg=self.default_entry_color)
        self.payload_size_Entry.config(fg=self.default_entry_color)
        self.payload_Entry.config(fg=self.default_entry_color)

    
    def add_to_Q(self):
        self.check_all_fields_completed()
        self.check_all_fields()
        self.fields_uncompleted_error()
        self.fields_completed_wrong_error()
        if self.check_all_fields_retVal == False and self.check_all_fields_completed_retVal == False:
            self.refresh_time()
            self.get_frame_data()
            self.listbox1.insert(self.position, self.string_max)
            self.initial_interface_state()
    
    def backend_module(self):
        if self.can_down_var:
            self.module.set_can_send_module_name(self.can_dict[self.can_sender_var.get()])
            self.module.set_can_receive_module_name(self.can_dict[self.can_receiver_var.get()])
            self.module.set_baudrate(self.baudrate_dict[self.drop_down_id_baudrate_var.get()])
            self.module.set_dbaudrate(self.baudrate_dict[self.drop_down_data_baudrate_var.get()])
            self.transmitter.interface_up(self.module.get_can_send_module_name(), self.module.get_baudrate(), self.module.get_dbaudrate())
            self.transmitter.interface_up(self.module.get_can_receive_module_name(), self.module.get_baudrate(), self.module.get_dbaudrate())
        else:
            self.transmitter.interface_down(self.module.get_can_send_module_name())
            self.transmitter.interface_down(self.module.get_can_receive_module_name())

    def backend_frame(self):
        self.Final_list = list(self.listbox1.get(0, END))
        for message in self.Final_list:
            index = 0
            for element in message:
                if element == "#":
                    break
                index += 1
            
            self.frame.set_id(message[10:index])
            self.frame.set_brs(message[index+2:index+3])
            self.frame.set_payload(message[index+4:])

    def send_que(self):
        if self.default_status_label.cget("text") == "UP":
            self.error_listbox.delete(0, END)
            self.module.send_q()
            self.backend_frame()
            print(f"{self.frame.id_list}{self.frame.payload_list}{self.frame.brs_list}")
        else:
            self.initial_interface_state()
            self.error_listbox.insert(END,"Error: CAN is DOWN")
            self.error_listbox.itemconfig(END, {'fg': 'red'})
