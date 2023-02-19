from tkinter import *
from tkinter.ttk import Progressbar
import time
from tkinter import ttk
import ast
import os
from tkinter import messagebox
import sys
#from tkmacosx import Button

class CANInterface():

    def __init__(self, gui_revision: str):
        self.gui_revision = gui_revision
        self.root = Tk("")
        self.root.title(f"CanInterfaceGUI {self.gui_revision}")
        self.root.iconbitmap("./Raspberry icon/Raspberry.ico")
        self.root.geometry("600x700")

        self.fd_box = IntVar()
        self.ext_box = IntVar()
        self.id_text = StringVar()
        self.baudrate_dict = {'100K':100,'200K':200,'400K':400,'500K':500,"1M":1,"2M":2,'3M':3,'4M':4,"5M":5,"8M":8}
        self.id_text.trace("w", self.frame_uncompleted)
        self.payload_size_entry = StringVar()
        self.payload_size_entry.trace("w", self.frame_uncompleted)
        self.payload_entry = StringVar()
        self.payload_entry.trace("w", self.frame_uncompleted)
        self.drop_down_menu_can = StringVar()
        self.drop_down_menu_can.set("Select")
        self.drop_down_menu_can.trace("w", self.can_frame_option_changed)
        self.drop_down_id_baudrate_var = StringVar()
        self.drop_down_id_baudrate_var.set("Select")
        self.drop_down_id_baudrate_var.trace("w", self.id_baudrate_option_changed)
        self.drop_down_data_baudrate_var = StringVar()
        self.drop_down_data_baudrate_var.set("Select")
        self.drop_down_data_baudrate_var.trace("w", self.data_baudrate_option_changed)
        self.position = 0
        self.can_interface_list = ('CAN0', 'CAN1')
        self.baudrate_list = ('100K','200K','400K','500K','1M','2M','5M','8M')
        self.data_baudrate_list = ('100K','200K','400K','500K','1M','2M','3M','4M','5M','6M','7M','8M')
        self.can_frame_changed = False
        self.can_down_var = True

    def build(self):
        self.can_frame1 = Frame(self.root, borderwidth=2, border=2)
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
        self.status_label.grid(row=0, column=3, padx=30, pady=(20,0))

        self.default_status_label = Label(self.can_frame1, text="DOWN", fg='red')
        self.default_status_label.grid(row=1, column=3, padx=30)

        self.send_button = Button(self.can_frame1, text="Send", command=self.progress_bar, state="normal")
        self.send_button.grid(row = 1, column=4, sticky='e')
        
        self.up_down_button = Button(self.can_frame1, text="UP",fg="green", command=self.up_down_button_command, width=3, state="disabled")
        self.up_down_button.grid(row=0, column=4, sticky='e')

        self.fd_Label = Label(self.can_frame2, text="Fd")
        self.fd_Label.grid(row= 0, column =0, padx=(40,0), pady=(50,0))

        self.fd_CkBt = Checkbutton(self.can_frame2, variable=self.fd_box, command= lambda: self.fd_box_checked())
        self.fd_CkBt.grid(row = 1, column=0, padx=(40,0), pady=(2,0))

        self.ext_flag_Label = Label(self.can_frame2, text="Ext")
        self.ext_flag_Label.grid(row =0 ,column=2, pady=(50,0))

        self.ext_flag_CkBt = Checkbutton(self.can_frame2, variable=self.ext_box)
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

        #self.pb = Progressbar(self.root, orient='horizontal', mode='determinate', length=63)
        #self.pb.grid(row = 2, column=7)

        self.add_to_q = Button(self.can_frame2, text="Add to q", command= self.add_to_Q, fg='red')
        self.add_to_q.grid(row = 1, column=6)

        self.listbox1.grid(row=0, column=0, padx=20, pady=(20,10))

        self.import_button = Button(self.can_frame4, text="Import", command = self.import_messagges)
        self.import_button.grid(row=0, column=0, padx=(20,0))

        self.save_button_input = Button(self.can_frame4, text="Save", command = self.save_messages_sent)
        self.save_button_input.grid(row=0, column=1, padx=10)

        self.clear_button_input = Button(self.can_frame4, text="Clear", command = lambda: self.delete_function(self.listbox1))
        self.clear_button_input.grid(row=0, column=2)

        self.listbox2.grid(row=0, column=0, padx=20, pady=(40,10))

        self.save_button_output = Button(self.can_frame6, text="Save", command=lambda:self.save_messages_received())
        self.save_button_output.grid(row=0, column=1, padx=(20,10))

        self.clear_button_output = Button(self.can_frame6, text="Clear", command = lambda: self.delete_function(self.listbox2))
        self.clear_button_output.grid(row=0, column=2)

        self.Error_label = Label(self.root, text = "")
        self.Error_label.grid(row = 1, column= 3)

        self.Edit_button = Button(self.can_frame4, text="Edit", command= self.edit_button)
        self.Edit_button.grid(row=0, column=3, padx=(30,10))

        self.ok_button = Button(self.can_frame4, text= "OK", command= self.ok_command)
        self.ok_button.grid(row=0, column=4)

    def up_down_button_command(self):
        self.cand_frame_changed
        
        if self.can_down_var:
            self.default_status_label.config(fg='green',text='UP')
            self.up_down_button.config(fg="red", text="DOWN")
            self.can_down_var = False
        else:
            self.default_status_label.config(fg='red',text='DOWN')
            self.up_down_button.config(fg="green", text= "UP")
            self.can_down_var = True

    def data_format(self, *args):
        self.string_data_format = self.payload_entry.get() + "."
        self.payload_entry = self.string_data_format
        print(self.string_data_format)

    def id_baudrate_option_changed(self, *args):
        self.id_baudrate_changed = True
        self.frame_uncompleted()

    def data_baudrate_option_changed(self, *args):
        self.data_baudrate_changed = True
        self.frame_uncompleted()

    def can_frame_option_changed(self, *args):
        self.can_frame_changed = True
        
    def delete_function(self, listbox):
        listbox.delete(ANCHOR)


    def ok_command(self):
        self.check_all_fields()
        if self.fd_box_retVal:
            self.Error_label.config(text="Error", fg='red')
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
                self.index_bd_first = 0
                self.index_bd_second = 0
                self.index_bd = 0
                self.value = self.listbox1.get(self.listbox1.curselection())
                print("1", self.value)
                self.value = self.value[10:]
                print("2", self.value)
                for element in self.value:
                    if element == "#":
                        print("here", type(element))
                        if self.value[self.value.index(element)+1] == "#":
                            self.index_element += 1
                        break
                    self.index_element += 1
                if self.value.count('/') == 2:
                    self.index_bd_first = self.value.index('/')
                    self.index_bd_second = self.index_bd_first
                    for element in self.value[self.index_bd_first+1:]:
                        if element == "/":
                            self.index_bd_second +=1
                            break
                        self.index_bd_second += 1
                    self.fd_CkBt.select()
                    self.drop_down_id_baudrate_var.set(self.value[self.index_bd_first+1:self.index_bd_second])
                    self.drop_down_data_baudrate_var.set(self.value[self.index_bd_second+1:])
                    self.drop_down_id_baudrate.config(state="normal")
                    self.drop_down_data_baudrate.config(state="normal")
                    
                print("1", self.value)
                print("2", self.index_element)
                print("3", self.index_bd_first)
                print("4", self.index_bd_second)

                    
                print("element", self.index_element)
                self.frame_id_entry.insert(0,self.value[0:self.index_element])
                self.payload_Entry.insert(0, self.value[self.index_element+1:self.index_bd_first])
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


    def frame_uncompleted(self, *args):
        self.frame_uncompleted_retVal = 0

        try:
            if self.can_frame_changed == True and self.id_baudrate_changed == True and self.data_baudrate_changed == True:
                self.up_down_button.config(state="normal")
        except:
            pass

        if self.ext_box.get() == 1:
            if len(self.payload_size_Entry.get()) != 0:
                pass
            else:
                self.frame_uncompleted_retVal = 1
                
        if len(self.frame_id_entry.get()) != 0 and len(self.payload_Entry.get()) != 0:
            pass
        else:
            self.frame_uncompleted_retVal = 1

        

        print("retvval", self.frame_uncompleted_retVal)
        print(self.id_text.get())


    def refresh_time(self):
        self.t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", self.t)

    def get_frame_data(self):
        if self.fd_box.get() == 1:
            print("what youa asked for", self.baudrate_dict[self.drop_down_data_baudrate_var.get()])
            self.string_max = self.current_time + "  " + self.frame_id_entry.get() + "#" + self.payload_entry.get() + "/" + self.drop_down_id_baudrate_var.get() + "/" + self.drop_down_data_baudrate_var.get()
            print(self.string_max)
            self.position += 1
        else:
            self.string_max = self.current_time + "  " + self.frame_id_entry.get() + "#" + self.payload_entry.get() 
            self.position += 1
        

    def fd_box_checked(self):
        self.fd_box_checked_retVal = False
        self.id_baudrate_changed = False
        self.data_baudrate_changed = False

        if self.fd_box.get() == 1:
            self.payload_size_Label.config(state="normal")
            self.payload_size_Entry.config(state="normal")
            self.fd_box_checked_retVal = True
        else:
            self.payload_size_Entry.delete(0, 'end')
            self.payload_size_Label.config(state="disabled")
            self.payload_size_Entry.config(state="disabled")

        self.frame_uncompleted()
    
    def save_messages_sent(self):
        with open("Messages_sent.txt","w") as f:
            for i in self.listbox1.get(0,END):
                f.write(i+"\n")

    def save_messages_received(self):
        with open("Messages_received.txt","w") as f:
            for i in self.listbox1.get(0,END):
                f.write(i+"\n")

    def check_all_fields(self):
        self.fd_box_retVal = False
        if self.ext_box.get() == 1:
            try:
                if int(self.frame_id_entry.get(), 16) < 2047:
                    self.fd_box_retVal = True
            except:
                    print("Not hexadecimal")
        else:
            try:
                if int(self.frame_id_entry.get(), 16) > 2047:
                    self.fd_box_retVal = True
            except:
                    print("Not hexadecimal")

    def initial_interface_state(self):
        self.Error_label.config(text="")   
        self.frame_id_entry.delete(0, 'end')
        self.payload_size_Entry.delete(0, 'end')
        self.payload_size_Label.config(state="disabled")
        self.payload_size_Entry.config(state="disabled", highlightbackground= "grey", borderwidth=1)
        self.payload_Entry.delete(0, 'end')
        self.fd_box.set(0)
        self.ext_box.set(0)

    def add_to_Q(self):
        self.check_all_fields()
        if self.fd_box_retVal:
            self.Error_label.config(text="Error", fg='red')
        else:
            self.refresh_time()
            self.get_frame_data()
            self.listbox1.insert(self.position, self.string_max)
            self.initial_interface_state()


    def progress_bar(self):
        self.Final_list = list(self.listbox1.get(0, END))
        print (self.Final_list)