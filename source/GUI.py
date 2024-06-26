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
import test_canbus as Can_Test
import psutil
import platform
import threading
from tkinter.filedialog import asksaveasfile
import random
from PIL import Image, ImageTk
import subprocess
import webbrowser
from collections import Counter
class CANGui():
    def __init__(self, gui_revision: str):
        self.splash()
        self.gui_revision = gui_revision
        self.root = Tk()
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        print('-', self.root.winfo_screenwidth(),'--', self.root.winfo_screenheight())
        self.root.title(f"CanInterfaceGUI {self.gui_revision}")
        #self.root.iconbitmap("./Raspberry icon/Raspberry.ico")
        
        # --- Menu Options
        self.menu_bar = Menu(self.root, bg="grey")
        self.general = Menu(self.menu_bar, tearoff = 0)
        self.view = Menu(self.menu_bar, tearoff = 0, bg="grey")
        self.help = Menu(self.menu_bar, tearoff = 0)

        self.general.add_command(label="About CANrasp", command=self.open_git_url)
        self.general.add_command(label="Check for Updates...", command=self.open_release_url)
        self.general.add_separator()
        self.cpu_sensor = Menu(self.general, tearoff=0)
        self.general.add_cascade(label="Sensors", menu=self.cpu_sensor)
        self.general.add_separator()
        self.general.add_command(label="Quit", command=self.root.destroy)
        self.view.add_command(label="Vertical", command=self.vertical_view)
        self.view.add_command(label="Horizontal", command = self.horizontal_view)
        self.help.add_command(label="Welcome", command = self.welcome_user)
        self.help.add_command(label="Contact", command = self.contact_msg)
        self.menu_bar.add_cascade(label="General", menu=self.general)
        self.menu_bar.add_cascade(label="View", menu=self.view)
        self.menu_bar.add_cascade(label="Help", menu=self.help)
        self.root.config(menu=self.menu_bar)
        # ---

        # --- Variable Initialization
        self.brs_box = IntVar()
        self.ext_box = IntVar()
        self.RTR_box = IntVar()
        self.FD_box = IntVar()
        self.que_loop_var = IntVar()
        self.id_text = StringVar()
        self.payload_entry = StringVar()
        self.payload_entry.set("")
        self.can_sender_var = StringVar()
        self.can_sender_var.set('Select')
        self.can_sender_var.trace("w", self.can_frame_option_changed)
        self.can_receiver_var = StringVar()
        self.can_receiver_var.set('Select')
        self.can_receiver_var.trace("w", self.can_frame_option_changed_1)
        self.drop_down_id_baudrate_var = StringVar()
        self.drop_down_id_baudrate_var.set("Select")
        self.drop_down_id_baudrate_var.trace("w", self.id_baudrate_option_changed)
        self.drop_down_data_baudrate_var = StringVar()
        self.drop_down_data_baudrate_var.set("Select")
        self.drop_down_data_baudrate_var.trace("w", self.data_baudrate_option_changed)
        self.see_only_dropdown_var = StringVar()
        self.see_only_dropdown_var.set('Test')
        self.see_only_dropdown_list = ('Echo', 'Negate', 'Increment', 'Decrement')
        self.text_variable_sp = StringVar()
        self.text_variable_sp.set("N/A")
        self.dtext_variable_sp = StringVar()
        self.position = 0
        self.can_send_module_optionmenu = None
        self.can_receive_module_optionmenu = None
        self.screen_width_h = self.root.winfo_screenwidth() // 23
        self.screen_height_h = self.root.winfo_screenheight() // 65
        self.screen_width_v = self.root.winfo_screenwidth() // 25
        self.screen_height_v = self.root.winfo_screenheight() // 100
        # ---

        # --- Platform Module
        if platform.system() == "Darwin":
            self.can_send_module_optionmenu = tuple(psutil.net_if_addrs())[1:4]
            self.can_receive_module_optionmenu = tuple(psutil.net_if_addrs())[1:4]
            self.can_dict = {'anpi0':"anpi0", 'anpi1':"anpi1", 'en0':"en0"}
        elif platform.system() == "Linux":
            self.can_send_module_optionmenu = tuple(filter(lambda item: item[:3] == 'can', os.listdir('/sys/class/net/')))
            self.can_receive_module_optionmenu = tuple(filter(lambda item: item[:3] == 'can', os.listdir('/sys/class/net/')))
            self.can_dict = {'CAN0':"can0", 'CAN1':"can1", 'CAN2':"can2"}
        else:
            self.can_send_module_optionmenu = ("CAN0", "CAN1")
            self.can_receive_module_optionmenu = ("CAN0","CAN1")
            self.can_dict = {'CAN0':"can0", 'CAN1':"can1", 'CAN2':"can2"}
        # ---

        self.baudrate_list = ('100K','200K','400K','500K','1M')
        self.data_baudrate_list = ('100K','200K','400K','500K','1M','2M','3M','4M','5M','6M','7M','8M')
        self.baudrate_dict = {'100K':100000,'200K':200000,'400K':400000,'500K':500000,"1M":1000000,"2M":2000000,'3M':3000000,'4M':4000000,"5M":5000000,"6M":6000000,"7M":7000000,"8M":8000000}   
        self.can_frame_changed = False
        self.frame = CAN_frame.CanFrame()
        self.module_sender = CAN_module.CanModule()
        self.module_receiver = CAN_module.CanModule()
        self.program_running = True
        self.chg_var = 0
        self.chg_var1 = 0
        self.list_read = []
        self.list_mem = []
        self.thread_error = False
        with open(self.module_sender.get_rasp_path()+'can.log', 'w') as f:
                pass
        with open(self.module_sender.get_rasp_path()+'status.txt', 'w') as f:
                pass
        self.cpu_temp = '0'
        self.dmessage = StringVar()
        self.dev_status = False
        self.root_dev = None
        self.delay_entry_var = IntVar()
        self.delay_optionmenu = ("1s","2s","3s","5s")
        self.delay_optionmenu_dict = {'1s':1, '2s':2, '3s':3, '5s':5}
        self.messages_loop_var = IntVar()
        self.loop_active = False
        self.active_loop_var = False

        # --- Threads
        t1 = threading.Thread(target=self.threadfunc, daemon=True)
        t1.start()
        t2 = threading.Thread(target=self.loop_section_button, daemon=True)
        t2.start()
        t3 = threading.Thread(target=self.que_loop, daemon=True)
        t3.start()
        t4 = threading.Thread(target=self.sensor_temp, daemon=True)
        t4.start()
        t5 = threading.Thread(target=self.temp_var_color, daemon=True)
        t5.start()
        t6 = threading.Thread(target=self.credential_offset, daemon=True)
        t6.start()
        # ---

        self.test_mode1 = StringVar()
        self.negate = StringVar()
        self.increment = StringVar()
        self.decrement = StringVar()

    def build(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.can_frame1 = Frame(self.root)
        self.can_frame1.grid(row=0, column=0, sticky="nsew")

        self.can_frame1_1 = Frame(self.can_frame1)
        self.can_frame1_1.grid(row=0, column=3, sticky="nsew")

        self.can_frame1_2 = Frame(self.can_frame1)
        self.can_frame1_2.grid(row=1, column=3, sticky="nsew")

        self.can_frame1_3 = Frame(self.can_frame1)
        self.can_frame1_3.grid(row=2, column=3, sticky="nsew")

        self.can_frame1_4 = Frame(self.can_frame1)
        self.can_frame1_4.grid(row=0, column=4, sticky="nsew")

        self.can_frame1_5 = Frame(self.can_frame1)
        self.can_frame1_5.grid(row=1, column=4, sticky="nsew")

        self.can_frame2 = Frame(self.root)
        self.can_frame2.grid(row=1, column=0, pady=15, sticky="nsew")

        self.can_frame3 = Frame(self.root)
        self.can_frame3.grid(row=2, column=0, sticky="nsew")

        self.can_frame4 = Frame(self.root)
        self.can_frame4.grid(row=3, column=0, sticky="nsew")

        self.empty_can_frame1 = Frame(self.root)
        self.empty_can_frame1.grid(row=1, column=1)

        self.can_frame5= Frame(self.root)
        self.can_frame5.grid(row=2, column=1, sticky="nsew")

        self.can_frame6 = Frame(self.root)
        self.can_frame6.grid(row=3, column=1, sticky="nsew")

        self.can_frame7 = Frame(self.root)
        self.can_frame7.grid(row=4, column=0, sticky="nsew", pady=(30))

        self.can_frame7_2 = Frame(self.can_frame7)
        self.can_frame7_2.grid(row=0, column=1)

        self.can_frame8 = Frame(self.can_frame7)
        self.can_frame8.grid(row=1, column=1, sticky="nw")

        self.empty_can_frame2 = Frame(self.root)
        self.empty_can_frame2.grid(row=1, column=3)

        self.can_frame9 = Frame(self.can_frame5)
        self.can_frame9.grid(row=0, column=1)

        self.can_frame12 = Frame(self.root)
        self.can_frame12.grid(row=0, column=2, sticky='nsew')

        # frame 1
        self.can_interface_sender_label = Label(self.can_frame1, text = "CAN SENDER")
        self.can_interface_sender_label.grid(row=0, column=0, padx=20, pady=(20,0))

        self.sender_drop_down_menu = OptionMenu(self.can_frame1, self.can_sender_var, *self.can_send_module_optionmenu)
        self.sender_drop_down_menu.config(width=5)
        self.sender_drop_down_menu.grid(row = 1, column = 0)

        self.can_interface_receiver_label = Label(self.can_frame1, text = "CAN RECEIVER")
        self.can_interface_receiver_label.grid(row=2, column=0)

        self.receiver_drop_down_menu = OptionMenu(self.can_frame1, self.can_receiver_var, *self.can_receive_module_optionmenu)
        self.receiver_drop_down_menu.config(width=5)
        self.receiver_drop_down_menu.grid(row = 3, column = 0)

        self.id_baudrate_Label = Label(self.can_frame1, text = "ID Baudrate")
        self.id_baudrate_Label.grid(row=0, column=1, pady=(20,0))

        self.drop_down_id_baudrate = OptionMenu(self.can_frame1,  self.drop_down_id_baudrate_var, *self.baudrate_list)
        self.drop_down_id_baudrate.config(width=5)
        self.drop_down_id_baudrate.grid(row = 1, column=1)

        self.data_baudrate_Label = Label(self.can_frame1, text = "DATA Baudrate")
        self.data_baudrate_Label.grid(row=0, column=2, pady=(20,0))

        self.drop_down_data_baudrate = OptionMenu(self.can_frame1, self.drop_down_data_baudrate_var, *self.data_baudrate_list)
        self.drop_down_data_baudrate.config(width=5)
        self.drop_down_data_baudrate.grid(row = 1, column=2)

        self.temp_cpu_label= Label(self.can_frame1, text= self.cpu_temp, width= 15)
        self.temp_cpu_label.grid(row=3, column=1)

        # frame_1_1
        self.sample_point_label = Label(self.can_frame1_1, text = "ID SP")
        self.sample_point_label.config(state='disabled')
        self.sample_point_label.grid(row=0, column=0, padx=(50,0), pady=(20,0))

        self.dsample_point_label = Label(self.can_frame1_1, text = "DATA SP")
        self.dsample_point_label.grid(row=0, column=1, padx=(77,0), pady=(20,0))

        # frame 1_2
        self.sample_point_entry = Entry(self.can_frame1_2, textvariable = self.text_variable_sp)
        self.sample_point_entry.config(width=5, state='disable')
        self.sample_point_entry.grid(row=0, column=0, padx=(47,0))

        self.dsample_point_entry = Entry(self.can_frame1_2, textvariable = self.dtext_variable_sp)
        self.dsample_point_entry.config(width=5)
        self.dsample_point_entry.grid(row=0, column=1, padx=(74,0))

        # frame 1_3
        self.actual_data_label = Label(self.can_frame1_3, text="Actual Data", font=('Arial', 10))
        self.actual_data_label.config(state='disabled')
        self.actual_data_label.grid(row=0, column=0, padx=(15,0))

        self.sample_point_data = Label(self.can_frame1_3, text = "0.750", font=('Arial', 10))
        self.sample_point_data.config(state='disabled')
        self.sample_point_data.grid(row=0, column=1)

        self.actual_data_dlabel = Label(self.can_frame1_3, text="Actual Data", font=('Arial', 10))
        self.actual_data_dlabel.grid(row=0, column=2, padx=(15,0))

        self.sample_dpoint_data = Label(self.can_frame1_3, text = "0.750", font=('Arial', 10))
        self.sample_dpoint_data.grid(row=0, column=3)

        # frame 1_4
        self.status_label = Label(self.can_frame1_4, text="STATUS")
        self.status_label.grid(row=0, column=0, pady=(20,0), padx=(self.root.winfo_screenwidth() - 1890,0))

        self.up_down_button = Button(self.can_frame1_4, text="UP",fg="green", command=self.up_down_button_command, width=3, state="disabled")
        self.up_down_button.grid(row=0, column=1, sticky='e', padx=(5,0), pady= (10,0))

        # frame 1_5
        self.default_status_label = Label(self.can_frame1_5, text="DOWN", fg='red')
        self.default_status_label.config(width=5)
        self.default_status_label.grid(row=0, column=0, padx=(30,0), sticky='e')
        
        self.dev_button = Button(self.can_frame1_5, text= "<  >", command=self.developer_settings, width = 3)
        self.dev_button.grid(row=0, column=1, padx=(10,0))

        # frame 2
        self.RTR_Label = Label(self.can_frame2, text="RTR")
        self.RTR_Label.grid(row= 0, column =0, padx=(20,0))

        self.RTR_CkBtn = Checkbutton(self.can_frame2, variable=self.RTR_box, command=self.rtr_function)
        self.RTR_CkBtn.grid(row = 1, column=0, padx=(20,0))

        self.brs_Label = Label(self.can_frame2, text="BRS")
        self.brs_Label.config(state='disable')
        self.brs_Label.grid(row= 0, column =1)

        self.brs_CkBt = Checkbutton(self.can_frame2, variable=self.brs_box)
        self.brs_CkBt.config(state='disable')
        self.brs_CkBt.grid(row = 1, column=1)

        self.ext_flag_Label = Label(self.can_frame2, text="EXT")
        self.ext_flag_Label.grid(row =0 ,column=2)

        self.ext_flag_CkBt = Checkbutton(self.can_frame2, variable=self.ext_box)
        self.ext_flag_CkBt.grid(row=1, column=2)

        self.ext_flag_Label = Label(self.can_frame2, text="FD")
        self.ext_flag_Label.grid(row= 0, column=3)

        self.FD_CkBtn = Checkbutton(self.can_frame2, variable=self.FD_box, command=self.fd_function)
        self.FD_CkBtn.grid(row = 1, column=3)

        self.frame_id_Label = Label(self.can_frame2, text="ID (0x)")
        self.frame_id_Label.grid(row = 0, column=4, padx=(5,0), sticky='w')
        self.default_label_color = self.frame_id_Label.cget('fg')

        self.frame_id_entry = Entry(self.can_frame2, textvariable=self.id_text, width= 10)
        self.frame_id_entry.grid(row = 1, column=4, padx=(5,0))
        self.default_entry_color = self.frame_id_entry.cget('fg')

        self.payload_Label = Label(self.can_frame2, text="PAYLOAD")
        self.payload_Label.grid(row = 0, column=5, sticky='w')

        self.payload_Entry = Entry(self.can_frame2, textvariable=self.payload_entry)
        self.payload_Entry.grid(row = 1, column=5)

        self.add_to_q = Button(self.can_frame2, text="ADD TO QUE", command= self.add_to_Q)
        self.add_to_q.grid(row = 1, column=6, padx=(238,0))

        # frame 3
        self.que_listbox_label = Label(self.can_frame3, text = "Message list")
        self.que_listbox_label.grid(row=0, column=0, sticky='w', padx=20)
        self.que_listbox_label.config(font=('Helvetica bold', 13))
    
        self.que_listbox = Listbox(self.can_frame3, yscrollcommand = 1, width = self.screen_width_h, height= self.screen_height_h, selectmode=EXTENDED)
        self.que_listbox.grid(row=1, column=0, padx=20)

        # frame 4
        self.import_button = Button(self.can_frame4, text="Import", command = self.import_messagges)
        self.import_button.grid(row=0, column=0, padx=(20,0))

        self.save_button_input = Button(self.can_frame4, text="Save", command = lambda:self.save("input"))
        self.save_button_input.grid(row=0, column=1)

        self.clear_button_input = Button(self.can_frame4, text="Clear", command = lambda: self.delete_function(self.que_listbox))
        self.clear_button_input.grid(row=0, column=2)

        self.Edit_button = Button(self.can_frame4, text="Edit", command= self.edit_button_fr4)
        self.Edit_button.grid(row=0, column=3, padx=(30,0))

        self.ok_button = Button(self.can_frame4, text= "OK", command= self.ok_command_fr4, state="disable")
        self.ok_button.grid(row=0, column=4)

        self.loop_checkbox_label = Label(self.can_frame4, text="LOOP")
        self.loop_checkbox_label.grid(row = 0, column=5, padx=(self.root.winfo_screenwidth() - 1660,0))

        self.loop_checkbox = Checkbutton(self.can_frame4, variable= self.que_loop_var)
        self.loop_checkbox.grid(row = 0, column=6)

        self.send_button = Button(self.can_frame4, text="SEND QUE", command=self.send_que, state="normal")
        self.send_button.grid(row = 0, column=7)

        # frame 5
        self.can_bus_listbox_label = Label(self.can_frame5, text="CAN BUS")
        self.can_bus_listbox_label.grid(row=0, column=0, sticky='w', padx=20)
        self.can_bus_listbox_label.config(font=('Helvetica bold', 13))

        self.can_bus_listbox = Listbox(self.can_frame5, yscrollcommand = 1, width = self.screen_width_h, height= self.screen_height_h, selectmode =EXTENDED)
        self.can_bus_listbox.grid(row=1, column=0, padx=20)

        # frame 6
        self.save_button_output = Button(self.can_frame6, text="Save", command=lambda:self.save("output"))
        self.save_button_output.grid(row=0, column=0, padx=(20,0), sticky='w')

        self.clear_button_output = Button(self.can_frame6, text="Clear", command = lambda: self.delete_function(self.can_bus_listbox))
        self.clear_button_output.grid(row=0, column=1, sticky='w')
        
        self.can_bus_seeonly_optionemnu = OptionMenu(self.can_frame6, self.see_only_dropdown_var, *self.see_only_dropdown_list)
        self.can_bus_seeonly_optionemnu.config(width = 6, state='normal')
        self.can_bus_seeonly_optionemnu.grid(row=0, column=2, sticky='w')

        self.start_test_button = Button(self.can_frame6, text="Start Test", command = self.test_starter)
        self.start_test_button.grid(row=0, column=3, sticky='w')
        

        # frame 7
        self.error_listbox_label = Label(self.can_frame7, text='Info list')
        self.error_listbox_label.grid(row=0, column=0, sticky='w', padx=(20,0), pady=(10,0))
        self.error_listbox_label.config(font=('Helvetica bold', 13))

        self.error_listbox =Listbox(self.can_frame7, width = 50, height=7, selectmode=EXTENDED)
        self.error_listbox.grid(row=1, column= 0, padx=(20,0), pady=5)

        # frame 7_2
        self.loop_section_label = Label(self.can_frame7_2, text='RANDOM LOOP SECTION')
        self.loop_section_label.grid(row=0, column=0,padx=(80,0), pady=(10,0))
        self.loop_section_label.config(font=('Helvetica bold', 13))

        # frame 8
        self.delay_label = Label(self.can_frame8, text="DELAY (ms)")
        self.delay_label.grid(row=0, column=0, padx=(110,0))

        self.delay_entry = Entry(self.can_frame8, textvariable=self.delay_entry_var)
        self.delay_entry.config(width=6)
        self.delay_entry.grid(row=1, column=0, padx=(110,0))

        self.loop_msg_label = Label(self.can_frame8, text="MESSAGES")
        self.loop_msg_label.grid(row=0, column=1)

        self.loop_messages_entry = Entry(self.can_frame8, textvariable=self.messages_loop_var)
        self.loop_messages_entry.config(width=6)
        self.loop_messages_entry.grid(row=1, column=1)

        self.loop_start_button = Button(self.can_frame8, text="START", command= self.random_loop_start_func, width=5)
        self.loop_start_button.grid(row=2, column=0, padx=(110,0))

        # frame 12
        try:
            self.image_dimenion = PhotoImage(file="../images/Continental-Logo.png")
            self.continental_logo_width, self.continental_logo_height = self.image_dimenion.width(), self.image_dimenion.height()
            self.imagee = Image.open(r"/home/raspberry/CAN-Tester/images/Continental-Logo.png").resize((self.continental_logo_width+130, self.continental_logo_height+30), Image.ANTIALIAS)
            self.imagee = ImageTk.PhotoImage(self.imagee)
            self.label1 = Label(self.can_frame12, image= self.imagee)
            self.label1.grid(row=0, column=0, padx=10, pady=(50,0))
        except:
            self.label1 = Label(self.can_frame12, text= 'Missing Continental Logo Image\nPlease contact developer,git\nbelow you can find e-mail address')
            self.label1.grid(row=0, column=0, padx=10, pady=(50,0))

    def build2(self):
        self.dev_can_frame_1 = Frame(self.root_dev)
        self.dev_can_frame_1.grid(row=0, column=0, sticky="nsew")

        self.dev_can_frame_2 = Frame(self.root_dev)
        self.dev_can_frame_2.grid(row=1, column=0, padx=[5,0], pady=10, sticky="nsew")

        self.dev_can_frame_3 = Frame(self.root_dev)
        self.dev_can_frame_3.grid(row=2, column=0,padx=[5,0], sticky="nsew")

        self.top_label = Label(self.dev_can_frame_1, text="DEFAULT AREA")
        self.top_label.grid(row=0, column=0, pady=[10,0])
        self.top_label.config(font=('Helvetica bold', 13))

        self.default_up_button = Button(self.dev_can_frame_1, text="Default canup", command=self.default_canup, width=10)
        self.default_up_button.grid(row=1, column=0, padx=[5,0], pady=[10,0], sticky='w')

        self.default_candump_button = Button(self.dev_can_frame_1, text="Default candump", command=self.default_candump, width=10)
        self.default_candump_button.grid(row=2, column=0, padx=[5,0], sticky='w')

        self.default_settings = Button(self.dev_can_frame_1, text="Modules settings", command=self.default_module_settings, width=10)
        self.default_settings.grid(row=3, column=0, padx=[5,0], sticky='w')

        self.default_message = Button(self.dev_can_frame_1, text="1 message", command=self.default_message_func, width=10)
        self.default_message.grid(row=1, column=1, pady=[10,0],sticky='w')

        self.top2_label = Label(self.dev_can_frame_2, text="MANUAL AREA")
        self.top2_label.grid(row=0, column=0, sticky='w')
        self.top2_label.config(font=('Helvetica bold', 13))

        self.message_label = Label(self.dev_can_frame_2, text="Message")
        self.message_label.grid(row=1, column=0, sticky='w')

        self.message_entry = Entry(self.dev_can_frame_2, textvariable=self.dmessage)
        self.message_entry.grid(row=2, column=0, sticky='w')

        self.top3_label = Label(self.dev_can_frame_3, text="STATUS AREA")
        self.top3_label.grid(row=0, column=0, sticky='w')
        self.top3_label.config(font=('Helvetica bold', 13))

        self.debugging_label = Label(self.dev_can_frame_3, text="DEBUGGING")
        self.debugging_label.grid(row=1, column=0, pady=[5,0])

        self.status_listbox = Listbox(self.dev_can_frame_3, width = 40)
        self.status_listbox.grid(row=2, column=0, padx=10)

        self.current_status_label = Label(self.dev_can_frame_3, text="CURRENT STATUS")
        self.current_status_label.grid(row=3, column=0, pady=[5,0])

        self.status_listbox = Listbox(self.dev_can_frame_3, width = 40)
        self.status_listbox.grid(row=4, column=0, padx=10)

    def find_bus_payload(self):
        simplified_id_list = []
        simplified_payload_list = []
        can_bus_list = list(self.can_bus_listbox.get(0, 'end'))
        for item in can_bus_list:
            left_sb_index = item.find('[')
            right_sb_index = item.find(']')
            sf_id = ((item[:left_sb_index]).strip())[4:].strip()
            sf_payload = item[right_sb_index+1:].strip()
            simplified_id_list.append(sf_id)
            simplified_payload_list.append(sf_payload)
            #print(simplified_id_list)
            #print(simplified_payload_list)
        return simplified_id_list, simplified_payload_list

    def info_listbox_testmode(self):
        test_number, x = self.find_bus_payload()
        self.error_listbox.delete(0, END)
        self.error_listbox.insert(END,'All messages ' + str(len(test_number)//2))
        self.error_listbox.itemconfig(END, {'fg': 'black'})
        self.error_listbox.insert(END,'Passed ' + str(len(self.pass_test_list)))
        self.error_listbox.itemconfig(END, {'fg': 'green'})
        self.error_listbox.insert(END,'Failed ' + str(len(self.error_test_list)))
        self.error_listbox.itemconfig(END, {'fg': 'red'})

        for i in range(len(test_number)):
            self.can_bus_listbox.itemconfig(i, {'fg': 'black'})

        if len(self.error_test_list) != 0:
            for i in range (len(self.error_test_list)):
                self.can_bus_listbox.itemconfig(self.error_test_list[i], {'fg': 'red'})
        else:
            for i in range(len(test_number)):
                self.can_bus_listbox.itemconfig(i, {'fg': 'black'})
            for i in range(len(self.pass_test_list)):
                self.can_bus_listbox.itemconfig(self.pass_test_list[i], {'fg': 'green'})

    def test_starter(self):
        id_list, payload_list = self.find_bus_payload()
        index = 0
        self.pass_test_list = []
        self.error_test_list = []
        
        can_test_mode = Can_Test.Test_Module()
        test_mode = self.see_only_dropdown_var.get()
        
        for i in range(len(id_list)//2):
            bytes_list = []
            if test_mode == 'Echo':
                if id_list[index] == id_list[index+1]:
                    if can_test_mode.echo(payload_list[index]) == payload_list[index+1]:
                        self.pass_test_list.append(index)
                    else:
                        self.error_test_list.append(index)
                index+=2
            if test_mode ==  'Increment':
                if id_list[index] == id_list[index+1]:
                    count = Counter(payload_list[index])
                    space_count = count[' ']
                    payload_len = len(payload_list[index])
                    nr_bytes = (payload_len  - space_count)//2
                    payload_list[index] = payload_list[index].replace(' ', '')
                    for i in range(nr_bytes*2):
                        if i % 2 !=0:
                            if i == 1:
                                bytes_list.append(payload_list[index][:i+1])
                            else:
                                bytes_list.append(payload_list[index][i-1:i+1])
                    print(can_test_mode.increment_payload(bytes_list))
                    print((payload_list[index+1].lower()).replace(' ',''))
                    if payload_list[index+1][0] == '0':
                        payload_list[index+1] = payload_list[index+1][1:]
                    if can_test_mode.increment_payload(bytes_list) == (payload_list[index+1].lower()).replace(' ',''):
                        self.pass_test_list.append(index)
                    else:
                        self.error_test_list.append(index)
                index+=2
            if test_mode ==  'Decrement':
                if id_list[index] == id_list[index+1]:
                    count = Counter(payload_list[index])
                    space_count = count[' ']
                    payload_len = len(payload_list[index])
                    nr_bytes = (payload_len - space_count)//2
                    payload_list[index] = payload_list[index].replace(' ', '')
                    for i in range(nr_bytes*2):
                        if i % 2 !=0:
                            if i == 1:
                                bytes_list.append(payload_list[index][:i+1])
                            else:
                                bytes_list.append(payload_list[index][i-1:i+1])
                    print('bytes_list',can_test_mode.decrement_payload(bytes_list))
                    print('next index',(payload_list[index+1].lower()).replace(' ',''))
                    time.sleep(2)
                    if payload_list[index+1][0] == '0':
                        print("here")
                        payload_list[index+1] = payload_list[index+1][1:]
                    if can_test_mode.decrement_payload(bytes_list) == (payload_list[index+1].lower()).replace(' ',''):
                        self.pass_test_list.append(index)
                    else:
                        self.error_test_list.append(index)
                index+=2
            if test_mode == 'Negate':
                if id_list[index] == id_list[index+1]:
                    #print('-', can_test_mode.negate_payload(payload_list[index].replace(' ','')) )
                    #print('--', payload_list[index+1].lower())
                    if can_test_mode.negate_payload(payload_list[index].replace(' ','')) == (payload_list[index+1].lower()).replace(' ',''):
                        self.pass_test_list.append(index)
                    else:
                        self.error_test_list.append(index)
                index+=2
        self.info_listbox_testmode()

    def open_git_url(self):
        webbrowser.open("https://github.com/timoothee/CAN-Tester")

    def open_release_url(self):
        webbrowser.open("https://github.com/timoothee/CAN-Tester/releases", new=0)

    def credential_offset(self):
        time.sleep(3)
        try:
            screen_height = self.root.winfo_screenheight()
            self.powered_offsety = (screen_height - self.error_listbox.winfo_rooty()) - 200
            print(self.powered_offsety)
            self.mail_offsety = (screen_height - self.save_button_output.winfo_rooty()) -310
            print(self.mail_offsety)
        except:
            time.sleep(2)

        self.can_frame10 = Frame(self.root, height=self.powered_offsety)
        self.can_frame10.grid(row=5, column=0, sticky='w')
        
        self.can_frame11 = Frame(self.root)
        self.can_frame11.grid(row=5, column=2, sticky='e')
        
        self.label = Label(self.can_frame10, text='Powered by: ICSolution', font='Helvetica 11 bold')
        self.label.grid(row=0, column=0, padx=(10,0),pady=(self.powered_offsety,0))
        
        self.label2 = Label(self.can_frame11, text='timotei.sandru@continental-corporation.com', font='Helvetica 11 bold')
        self.label2.grid(row=0, column=0, padx =10 , pady=(self.mail_offsety,0), sticky='e')
        
        
    def sensor_temp(self):
        slash_list = ['|','/','-','\\']
        time.sleep(1)
        for i in range(8):
            point_load = ''
            self.temp_cpu_label.config(text='CPU Temp')
            for i in range(4):
                point_load = slash_list[i]
                self.temp_cpu_label.config(text=point_load + ' CPU Temp ' + point_load)
                time.sleep(0.2)
        
        self.cpu_sensor.add_command(label="CPU")
        output = subprocess.check_output(['sensors'])
        if output.decode().split('\n')[2].split()[1] == 'N/A':
            x = 6
        else:
            x = 2
        while True:
            output = subprocess.check_output(['sensors'])
            self.temp_int = output.decode().split('\n')[x].split()[1]
            self.cpu_temp = "CPU "+ self.temp_int
            self.cpu_sensor.entryconfig(0,label=self.cpu_temp)
            self.temp_cpu_label.config(text='Temp '+self.cpu_temp)
            time.sleep(0.5)
        

    def temp_var_color(self):
        time.sleep(15)
        while True:
            temp_int = self.temp_int
            for char in temp_int:
                if char.isdigit() != True:
                    temp_int = temp_int.replace(char, '')
            temp_int = int(temp_int) / 10

            if int(temp_int) < 50:
                self.temp_cpu_label.config(fg=self.default_label_color)
            if int(temp_int) >= 50:
                self.temp_cpu_label.config(fg='#E39010')
            if int(temp_int) > 70:
                self.temp_cpu_label.config(fg='red')

    def contact_msg(self):
        messagebox.showinfo(title="INFO", message="Contact Teams: \nSandru Timotei")

    def welcome_user(self):
        self.case = 1
        self.welcome_root = Toplevel(self.root)
        self.welcome_fr1 = Frame(self.welcome_root)
        self.welcome_fr1.grid(row=0, column=0, pady=(300,0))
        self.welcome_fr2 = Frame(self.welcome_root)
        self.welcome_fr2.grid(row=1, column=0)
        self.welcome_root.geometry("800x550")
        self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/one.png')
        imagee = self.image.resize((800, 500), Image.ANTIALIAS)
        new_imagee = ImageTk.PhotoImage(imagee)
        self.label1 = Label(self.welcome_root, image= new_imagee)
        self.label.image=new_imagee
        self.label1.grid(row=0, column=0)
        self.welcome_root.geometry("800x550")
        self.next_button = Button(self.welcome_fr2, text="Next", command= self.case_scenario)
        self.next_button.grid(row=1, column=0, sticky='s')
        self.welcome_root.mainloop()

    def case_scenario(self):
        self.case += 1
        if self.case == 10:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/one.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
            self.welcome_root.geometry("800x550")
        if self.case == 2:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/two.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
            
        if self.case == 3:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/three.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
        if self.case == 4:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/four.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
            
        if self.case == 5:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/five.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
            
        if self.case == 6:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/six.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
            
        if self.case == 7:
            self.image = Image.open('/home/raspberry/CAN-Tester/images/welcome/seven.png')
            imagee = self.image.resize((800, 500), Image.ANTIALIAS)
            new_imagee = ImageTk.PhotoImage(imagee)
            self.label1 = Label(self.welcome_root, image= new_imagee)
            self.label.image=new_imagee
            self.label1.grid(row=0, column=0)
           
            self.next_button.config(text='Close')
        if self.case == 8:
            self.welcome_root.destroy()


    def vertical_view(self):
        self.can_frame5.grid(row=4, column=0, sticky="nsew")
        self.can_frame6.grid(row=5, column=0, sticky="nsew")
        self.can_frame7.grid(row=6, column=0, sticky="nsew", pady=(30))
        self.can_frame7_2.grid(row=0, column=1)
        self.can_frame8.grid(row=1, column=1, sticky="nw")
        self.que_listbox.configure(width = self.root.winfo_width() - 1845, height= 10)
        self.can_bus_listbox.configure(width = self.root.winfo_width() - 1845, height= 10)
        self.root.geometry("750x1200")
        self.add_to_q.grid(padx=(self.root.winfo_width() - 1760,0))
        self.loop_checkbox_label.grid(padx=(187,0))
        self.status_label.grid(row=0, column=0, pady=(20,0), padx=(10,0))
        self.default_status_label.grid(row=0, column=0, padx=(13,0), sticky='e')
        self.loop_section_label.grid(padx=(50,0))
        self.delay_label.grid(padx=(80,0))
        self.delay_entry.grid(padx=(80,0))
        self.loop_start_button.grid(padx=(90,0))
        self.can_frame10.grid_forget()
        self.can_frame11.grid_forget()
        self.label.grid_forget()
        self.label1.grid_forget()
        
        self.label = Label(self.can_frame7, text='Powered by: ICSolution', font='Helvetica 11 bold')
        self.label.grid(row=2, column=0, sticky='w', padx=(20,0), pady=(30,0))
        self.imagee = Image.open(r"/home/raspberry/CAN-Tester/images/Continental-Logo.png").resize((self.continental_logo_width, self.continental_logo_height), Image.ANTIALIAS)
        self.imagee = ImageTk.PhotoImage(self.imagee)
        self.label1 = Label(self.can_frame7, image= self.imagee)
        self.label1.grid(row=2, column=1, padx=(10,0))
        #self.label2 = Label(self.can_frame8, text='timotei.sandru@continental-corporation.com', font='Helvetica 11 bold')
        #self.label2.grid(row=3, column=0, sticky='e')
        
    
    def horizontal_view(self):
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.can_frame1.grid(row=0, column=0, sticky="nsew")
        self.can_frame1_1.grid(row=0, column=3, sticky="nsew")
        self.can_frame1_2.grid(row=1, column=3, sticky="nsew")
        self.can_frame1_3.grid(row=2, column=3, sticky="nsew")
        self.can_frame1_4.grid(row=0, column=4, sticky="nsew")
        self.status_label.grid(row=0, column=0, pady=(20,0), padx=(self.root.winfo_screenwidth() - 1890,0))
        self.default_status_label.grid(row=0, column=0, padx=(30,0), sticky='e')
        self.can_frame1_5.grid(row=1, column=4, sticky="nsew")
        self.can_frame2.grid(row=1, column=0, pady=15, sticky="nsew")
        self.can_frame3.grid(row=2, column=0, sticky="nsew")
        self.can_frame4.grid(row=3, column=0, sticky="nsew")
        self.empty_can_frame1.grid(row=1, column=1)
        self.can_frame5.grid(row=2, column=1, sticky="nsew")
        self.can_frame6.grid(row=3, column=1, sticky="nsew")
        self.can_frame7.grid(row=4, column=0, sticky="nsew", pady=(30))
        self.can_frame7_2.grid(row=0, column=1)
        self.can_frame8.grid(row=1, column=1, sticky="nw")
        self.que_listbox.configure(width = self.screen_width_h, height= self.screen_height_h)
        self.can_bus_listbox.configure(width = self.screen_width_h, height= self.screen_height_h)
        self.add_to_q.grid(row = 1, column=6, padx=(238,0))
        self.loop_checkbox_label.grid(padx=(self.root.winfo_screenwidth() - 1660,0))
        self.loop_section_label.grid(padx=(80,0))
        self.delay_label.grid(padx=(110,0))
        self.delay_entry.grid(padx=(110,0))
        self.loop_start_button.grid(padx=(110,0))
        self.can_frame10.grid_forget()
        self.can_frame11.grid_forget()
        self.label.grid_forget()
        self.label1.grid_forget()
        self.imagee = Image.open(r"/home/raspberry/CAN-Tester/images/Continental-Logo.png").resize((self.continental_logo_width+130, self.continental_logo_height+30), Image.ANTIALIAS)
        self.imagee = ImageTk.PhotoImage(self.imagee)
        self.label1 = Label(self.can_frame12, image= self.imagee)
        self.label1.grid(row=0, column=0, padx=10, pady=(50,0))
        screen_height = self.root.winfo_screenheight()
        self.can_frame10 = Frame(self.root, height=self.powered_offsety)
        self.can_frame10.grid(row=5, column=0, sticky='w')
        self.can_frame11 = Frame(self.root)
        self.can_frame11.grid(row=5, column=2, sticky='e')
        self.label = Label(self.can_frame10, text='Powered by: ICSolution', font='Helvetica 11 bold')
        self.label.grid(row=0, column=0, padx=(10,0),pady=(self.powered_offsety,0))
        self.label2 = Label(self.can_frame11, text='timotei.sandru@continental-corporation.com', font='Helvetica 11 bold')
        self.label2.grid(row=0, column=0, padx =10 , pady=(self.mail_offsety,0), sticky='e')
    def que_loop(self):
        time.sleep(10)
        while True:
            while self.que_loop_var.get() == 1 and self.active_loop_var == True:
                for item in list(self.que_listbox.get(0, 'end')):
                    self.module_sender.random_message(str(item[10:]))
                time.sleep(1)
                if self.que_loop_var.get() != 1:
                    self.active_loop_var = False
            self.module_sender.default_led()

    def splash(self):
        root = Tk()
        splash = SplashScreen(root)
        for i in range(200):
            if i % 10 == 0:
                splash.config_splash()
            root.update()
            splash.progressbar.step(0.5)
            time.sleep(0.01)
        splash.destroy()
        root.mainloop()

    def random_loop_start_func(self):
        self.check_random_loop()
        self.random_loop_error_list()
        self.loop_active = True

    def check_random_loop(self):
        self.delay_entry_incomplete = False
        self.messages_entry_incomplete = False
        self.delay_entry_wrong = False
        self.messages_entry_wrong = False

        if isinstance(self.delay_entry_var.get(), int) == False:
            self.delay_entry_wrong = True
        if isinstance(self.messages_loop_var.get(), int) == False:
            self.messages_entry_wrong = True
        if self.delay_entry_var.get() == 0 and self.delay_entry_wrong == False:
            self.delay_entry_incomplete = True
        if self.messages_loop_var.get() == 0 and self.messages_entry_wrong == False:
            self.messages_entry_incomplete = True

    def random_loop_error_list(self):
        if self.delay_entry_incomplete == True:
            self.error_listbox.insert(END,"Error: Delay field uncompleted")
            self.error_listbox.itemconfig(END, {'fg': 'red'})
            self.frame_id_entry.config(fg= 'red')
        if self.messages_entry_incomplete == True:
            self.error_listbox.insert(END,"Error: Messages field uncompleted")
            self.error_listbox.itemconfig(END, {'fg': 'red'})
            self.frame_id_entry.config(fg= 'red')
        if self.delay_entry_wrong == True:
            self.error_listbox.insert(END,"Error: Delay field")
            self.error_listbox.itemconfig(END, {'fg': 'red'})
            self.frame_id_entry.config(fg= 'red')
        if self.messages_entry_wrong == True:
            self.error_listbox.insert(END,"Error: Messages field")
            self.error_listbox.itemconfig(END, {'fg': 'red'})
            self.frame_id_entry.config(fg= 'red')

    def loop_section_button(self):
        while True:
            if self.loop_active == True:
                if self.default_status_label.cget("text") == "UP":
                    for i in range(self.messages_loop_var.get()):
                        random_message = ""
                        bits_list = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

                        if random.choice(['normal', 'extended']) == "normal":
                            random_message = random.choice(['1','2','3','4','5','6','7']) + random.choice(bits_list) + random.choice(bits_list)
                        else:
                            random_message = '1'
                            for i in range(7):
                                random_message = random_message + random.choice(bits_list)
                        random_message = random_message + "##" + str(random.randrange(0, 9))

                        for i in range(random.randrange(1,11,2)+1):
                            random_message = random_message + random.choice(bits_list)

                        self.module_sender.random_message(random_message)
                        time.sleep(self.delay_entry_var.get()/1000)
                    self.loop_active = False
                else:
                    self.error_listbox.insert(END,"Error: CAN is DOWN")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.loop_active = False
            self.module_sender.default_led()
    
    def default_module_settings(self):
        self.can_sender_var.set("can0")
        self.can_receiver_var.set("can1")
        self.drop_down_id_baudrate_var.set("1M")
        self.drop_down_data_baudrate_var.set("5M")

    def debugging(self, message, color):
        if self.root_dev is None or not self.root_dev.winfo_exists():
            self.refresh_time()
            status_message = self.current_time + " " + message
            with open('../logs/status.txt', 'a+') as f:
                f.write(status_message+'\n')
        else:
            self.refresh_time()
            status_message = self.current_time + " " + message
            self.status_listbox.insert('end', status_message)
            if color == 1:
                self.status_listbox.itemconfig('end', {'fg': 'red'})
            if color == 2:
                self.status_listbox.itemconfig('end', {'fg': 'green'})
            self.status_listbox.see(END)

    def rtr_function(self):
        if self.RTR_box.get() == 1:
            self.payload_Entry.config(state="readonly")
            self.payload_Label.config(state="disabled")
        else:
            self.payload_Entry.config(state="normal")
            self.payload_Label.config(state="normal")

    def fd_function(self):
        if self.FD_box.get() == 1:
            self.brs_Label.config(state="normal")
            self.brs_CkBt.config(state='normal')
        else:
            self.brs_Label.config(state="disabled")
            self.brs_CkBt.config(state='disabled')

    def developer_send_func(self, event):
        os.popen(self.message_entry.get())

    def developer_settings(self):
        self.root_dev = Toplevel(self.root)
        self.root_dev.title("Develop settings")
        self.root_dev.geometry("500x600+650+0")
        self.build2()
        self.dev_status = True
        self.root_dev.bind('<Return>', self.developer_send_func)
        self.dev_status = False
    
    def default_message_func(self):
        self.module_sender.default_message_func()

    def default_canup(self):
        self.module_sender.default_canup()

    def default_candump(self):
        self.module_sender.default_candump()

    def on_closing(self):
        self.module_sender.interface_down()
        self.module_receiver.interface_down()
        self.program_running = False
        self.root.destroy() 

    def interface_up_disable_user(self):
        self.can_interface_sender_label.config(state='disable')
        self.sender_drop_down_menu.config(state='disable')
        self.can_interface_receiver_label.config(state='disable')
        self.receiver_drop_down_menu.config(state='disable')
        self.id_baudrate_Label.config(state='disable')
        self.drop_down_id_baudrate.config(state='disable')
        self.data_baudrate_Label.config(state='disable')
        self.drop_down_data_baudrate.config(state='disable')
        self.sample_point_entry.config(state='disable')
        self.dsample_point_entry.config(state='disable')
        time.sleep(1)

    def interface_up_enable_user(self):
        self.can_interface_sender_label.config(state='normal')
        self.sender_drop_down_menu.config(state='normal')
        self.can_interface_receiver_label.config(state='normal')
        self.receiver_drop_down_menu.config(state='normal')
        self.id_baudrate_Label.config(state='normal')
        self.drop_down_id_baudrate.config(state='normal')
        self.data_baudrate_Label.config(state='normal')
        self.drop_down_data_baudrate.config(state='normal')
        #self.sample_point_entry.config(state='normal')  # needs functionality
        self.dsample_point_entry.config(state='normal')
        time.sleep(1)


    def up_down_button_command(self):
        self.debugging("-- Inside up_down_button_command function --", 0)
        if self.module_sender.get_can_status() == False:
            self.module_sender.set_can_status(True)
            self.default_status_label.config(fg='green',text='UP')
            self.up_down_button.config(fg="red", text="DOWN")
            self.backend_module()
            self.initial_interface_state()
            self.debugging(" Status is UP", 2)
            self.interface_up_disable_user()
        else:
            self.module_sender.set_can_status(False)
            self.default_status_label.config(fg='red',text='DOWN')
            self.up_down_button.config(fg="green", text= "UP")
            self.backend_module()
            self.debugging(" Status is DOWN", 1)
            self.interface_up_enable_user()
        self.debugging("-- Leaving up_down_button_command function --", 0)

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
        self.chg_var1 += 1
        self.can_frame_changed_1 = True
        self.btn_up_down_active()
        
    def delete_function(self, listbox):
        self.debugging("DELETE", 0)
        if len(self.que_listbox.curselection()) != 0:
            listbox.delete(ANCHOR)
        else:
            listbox.delete(0, END)


    def threadfunc(self):
        while True:
            with open(self.module_sender.get_rasp_path()+'can.log', 'r') as f:
                self.list_read = f.readlines()
            if len(self.list_read) != len(self.list_mem):
                for i in range(len(self.list_mem) ,len(self.list_read)):
                    self.list_read[i] = self.list_read[i].replace(b'\x00'.decode(),'')
                    self.list_read[i] = self.list_read[i].replace(b'\n'.decode(),'')
                    #print("---", self.list_read)
                    #print("++",self.list_read[i].strip())
                    self.can_bus_listbox.insert('end', self.list_read[i])
                    self.can_bus_listbox.see(END) 
                self.list_mem = self.list_read

    def ok_command_fr4(self):
        self.debugging("-- Inside ok_command_fr4 function --", 0)
        self.check_all_fields_completed()
        self.check_all_fields()
        if self.check_all_fields_retVal:
            self.fields_uncompleted_error()
            self.fields_completed_wrong_error()
        else:
            self.refresh_time()
            self.get_frame_data()
            
            self.que_listbox.delete(self.our_item)
            self.que_listbox.insert(self.our_item, self.string_max)
            self.que_listbox.itemconfig(self.our_item, {'fg': 'green'})
            self.initial_interface_state()

        
    def edit_button_fr4(self):
        if self.que_listbox.size() != 0:
            if len(self.que_listbox.curselection()) != 0:
                self.initial_interface_state()
                self.ok_button.config(state="normal")
                self.our_item = self.que_listbox.curselection()
                self.index_element = 0
                self.value = self.que_listbox.get(self.que_listbox.curselection())[10:]
                for element in self.value:
                    if element == "#":
                        break
                    self.index_element += 1
                self.frame_id_entry.insert(0,self.value[0:self.index_element])
                self.payload_Entry.insert(0, self.value[self.index_element+3:])

                if int(self.frame_id_entry.get(), 16) > 2047:
                    self.ext_flag_CkBt.select()

                if self.value[self.index_element+1] != "R":
                    if self.value[self.index_element+2] == "1":
                        self.brs_CkBt.select()
                else:
                    self.RTR_CkBtn.select()
                    self.payload_Entry.config(state="disabled")
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

            self.refresh_time()
            for item in self.lines:
                self.string_import = self.current_time + "  " + item
                self.string_import = self.string_import.replace(b'\n'.decode(),'')
                self.que_listbox.insert('end', self.string_import)

    def btn_up_down_active(self, *args):
        try:
            if self.can_frame_changed == True and self.id_baudrate_changed == True and self.data_baudrate_changed == True and self.can_frame_changed_1 == True:
                self.up_down_button.config(state="normal")
        except:
            pass

    def check_all_fields_completed(self):
        self.debugging("... checking if all fields completed", 0)
        self.check_all_fields_completed_retVal = False
        self.id_entry_error = False
        self.payload_size_error = False
        self.payload_entry_error = False
        self.payload_entry_odd = False
        self.id_entry_over_error = False
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
        self.debugging("checking finished ...", 0)

    def check_all_fields(self):
        self.debugging("... checking if the fields are completed correctly", 0)
        self.check_all_fields_retVal = False
        self.zero_size = 0

        if self.RTR_box.get() == 1:
            if self.check_all_fields_completed_retVal == False:
                pass
            else:
                self.check_all_fields_completed_retVal = False
            
        if self.check_all_fields_completed_retVal:
            pass
        else:
            if self.ext_box.get() == 1:
                if int(self.frame_id_entry.get(), 16) < 2047:
                    self.id_entry_error = True
                    self.check_all_fields_retVal = True
                if int(self.frame_id_entry.get(), 16) > 536870911:
                    self.id_entry_over_error = True
                    self.check_all_fields_retVal = True
                if len(self.frame_id_entry.get())!= 8:
                    self.zero_size = 8 - int(len(self.frame_id_entry.get()))
            else:
                if int(self.frame_id_entry.get(), 16) > 2047:
                    self.id_entry_error = True
                    self.check_all_fields_retVal = True
                if len(self.frame_id_entry.get()) != 3:
                    self.zero_size = 3 - int(len(self.frame_id_entry.get()))
        if len(self.payload_entry.get())%2 != 0:
            self.payload_entry_odd = True
            self.check_all_fields_retVal = True

        self.debugging(" checking finished! ...", 0)

    def fields_uncompleted_error(self):
        self.error_listbox.delete(0,END)
        self.frame_id_Label.config(fg=self.default_label_color)
        self.payload_Label.config(fg=self.default_label_color)
        if self.check_all_fields_completed_retVal:
            self.debugging("... Not all fields were completed !", 1)
            if self.id_entry_error == True:
                self.frame_id_Label.config(fg='red')
                self.error_listbox.insert(END,"Error: Id uncompleted")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
            if self.payload_size_error == True:
                self.error_listbox.insert(END,"Error: Payload size uncompleted")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
            if self.payload_entry_error == True:
                self.payload_Label.config(fg='red')
                self.error_listbox.insert(END,"Error: Payload uncompleted")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
    
    def fields_completed_wrong_error(self):
        if self.check_all_fields_retVal == True:
            self.debugging("... Some fields were completed wrong ! ", 1)
            self.error_listbox.delete(0,END)
            self.frame_id_entry.config(fg=self.default_entry_color)
            self.payload_Entry.config(fg=self.default_entry_color)
            if self.id_entry_error == True or self.id_entry_over_error == True:
                if self.ext_box.get() == 1 and self.id_entry_over_error == False:
                    self.error_listbox.insert(END,"Error: Ext selected, Id not ext")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.frame_id_entry.config(fg= 'red')
                elif self.ext_box.get() == 1 and self.id_entry_over_error == True:
                    self.error_listbox.insert(END,"Error: Ext selected, Id exceeds limit")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.frame_id_entry.config(fg= 'red')
                if self.ext_box.get() == 0:
                    self.error_listbox.insert(END,"Error: Id ext")
                    self.error_listbox.itemconfig(END, {'fg': 'red'})
                    self.frame_id_entry.config(fg= 'red')
            if self.payload_size_error == True or self.payload_entry_error == True:
                self.error_listbox.insert(END,"Error: Payload not equal to payload size")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
                self.payload_Entry.config(fg= 'red')
            if self.payload_entry_odd:
                self.error_listbox.insert(END,"Error: Payload odd")
                self.error_listbox.itemconfig(END, {'fg': 'red'})
                self.payload_Entry.config(fg= 'red')
                

    def refresh_time(self):
        self.t = time.localtime()
        self.current_time = time.strftime("%H:%M:%S", self.t)

    def get_frame_data(self):
            zero_var = ''
            self.debugging(".. getting frame data", 0)
            if self.RTR_box.get() == 1:
                self.string_max = self.current_time + "  " + str(self.frame_id_entry.get()) + "#R"
                pass
            if self.FD_box.get() == 1 and self.zero_size == 0:
                self.string_max = self.current_time + "  " + str(self.frame_id_entry.get()) + "##" + str(self.brs_box.get()) + str(self.payload_entry.get())
                self.position += 1
            elif self.FD_box.get() == 1 and self.zero_size != 0:
                for i in range(self.zero_size):
                    zero_var += '0'
                self.string_max = self.current_time + "  " + zero_var + str(self.frame_id_entry.get()) + "##" + str(self.brs_box.get()) + str(self.payload_entry.get())
                self.position += 1
            if self.FD_box.get() == 0 and self.zero_size == 0:
                self.string_max = self.current_time + "  " + str(self.frame_id_entry.get()) + "#" + str(self.payload_entry.get())
                self.position += 1
            elif self.FD_box.get() == 0 and self.zero_size != 0:
                for i in range(self.zero_size):
                    zero_var += '0'
                self.string_max = self.current_time + "  " + zero_var +str(self.frame_id_entry.get()) + "#" + str(self.payload_entry.get())
                self.position += 1


    def save(self, mode):
        first_one = False
        self.debugging(".. saving data to file", 0)
        if mode == "input":
            self.debugging("input mode", 0)
            if self.que_listbox.size() != 0:
                files = [('All Files', '*.*'), ('Python Files', '*.py'), ('Text Document', '*.txt')]
                file = asksaveasfile(filetypes = files, defaultextension = files, mode = 'w')
                self.debugging(".. file asked", 0)
                if not file:
                    pass
                else:
                    self.debugging("file selected", 0)
                    lista = list(self.que_listbox.get(0, END))
                    for item in lista:
                        item = item[10:]
                        if first_one == False:
                            first_one = True
                            file.write(item)
                            continue
                        file.write('\n')
                        file.write(item)
                    file.close()
            else:
                messagebox.showerror("Status", "List is empty")
            

        else:
            self.debugging("output mode", 0)
            if self.can_bus_listbox.size() != 0:
                files = [('All Files', '*.*'), ('Python Files', '*.py'), ('Text Document', '*.txt')]
                filename = asksaveasfile(filetypes = files, defaultextension = files)
                lista = list(self.can_bus_listbox.get(0, END))
                if filename:
                    f = open(filename.name, 'w')
                    for item in lista:
                        if first_one == False:
                            first_one = True
                            f.write(item)
                            continue
                        f.write('\n')
                        f.write(item)
                    f.close()
                else:
                    messagebox.showerror("Status", "Error with filename")
            else:
                messagebox.showerror("Status", "List is empty")

    def initial_interface_state(self):
        self.debugging("setting all to default", 0)
        self.ok_button.config(state="disable")
        self.RTR_box.set(0)
        self.brs_box.set(0)
        self.ext_box.set(0)   
        self.frame_id_entry.delete(0, 'end')
        self.payload_Entry.delete(0, 'end')
        self.error_listbox.delete(0,END)
        self.frame_id_Label.config(fg=self.default_label_color)
        self.payload_Label.config(fg=self.default_label_color, state="normal")
        self.frame_id_entry.config(fg=self.default_entry_color)
        self.payload_Entry.config(fg=self.default_entry_color, state="normal")
        
    def add_to_Q(self):
        self.check_all_fields_completed()
        self.check_all_fields()
        self.fields_uncompleted_error()
        self.fields_completed_wrong_error()
        if self.check_all_fields_retVal == False and self.check_all_fields_completed_retVal == False:
            self.debugging(".. all went good ", 0)
            self.refresh_time()
            self.get_frame_data()
            self.que_listbox.insert(self.position, self.string_max)
            self.initial_interface_state()
        else:
            self.debugging("Something went wrong !", 1)
    
    def backend_module(self):
        if self.module_sender.get_can_status() == True:
            self.debugging("User wants to set CAN UP", 0)
            self.module_sender.set_module_name(self.can_sender_var.get())
            self.module_receiver.set_module_name(self.can_receiver_var.get())
            self.module_sender.set_baudrate(self.baudrate_dict[self.drop_down_id_baudrate_var.get()])
            self.module_sender.set_dbaudrate(self.baudrate_dict[self.drop_down_data_baudrate_var.get()])
            self.module_receiver.set_baudrate(self.baudrate_dict[self.drop_down_id_baudrate_var.get()])
            self.module_receiver.set_dbaudrate(self.baudrate_dict[self.drop_down_data_baudrate_var.get()])
            self.module_sender.interface_down()
            self.module_receiver.interface_down()
            self.module_sender.set_dsample_point(self.dtext_variable_sp.get())
            self.module_receiver.set_dsample_point(self.dtext_variable_sp.get())
            time.sleep(1)
            self.module_sender.interface_up()
            self.module_receiver.interface_up()
            time.sleep(1)
            self.module_receiver.can_dump()
            sample_point = self.module_sender.get_dsample_point()
            try:
                self.sample_dpoint_data.config(text=sample_point)
            except:
                pass
        else:
            self.debugging(" User wants to set CAN DOWN", 0)
            self.module_sender.interface_down()
            self.module_receiver.interface_down()

    def backend_frame(self):
        self.backend_list = list(self.que_listbox.get(0, END))
        self.frame.id_list.clear()
        self.frame.brs_list.clear()
        self.frame.payload_list.clear()
        self.frame.fd_list.clear()
        for message in self.backend_list:
            rtr_mode = "disabled"
            fd_mode = "active"
            index = 0
            for element in message:
                if element == "#":
                    if message[index+1] == "R":
                        rtr_mode = "active"
                    if message[index+1] != "#":
                        fd_mode = "disabled"
                    break
                index += 1
            if rtr_mode == "active":
                self.frame.set_id(message[10:index])
                self.frame.set_brs("")
                self.frame.set_payload(message[index+1:])
                self.frame.set_fd_flag("0")
            if fd_mode == 'active':
                self.frame.set_id(message[10:index])
                self.frame.set_brs(message[index+2:index+3])
                self.frame.set_payload(message[index+3:])
                self.frame.set_fd_flag("1")
            else:
                self.frame.set_id(message[10:index])
                self.frame.set_brs("")
                self.frame.set_payload(message[index+1:])
                self.frame.set_fd_flag("0")
            
            

    def send_que(self):
        if self.default_status_label.cget("text") == "UP":
            self.error_listbox.delete(0, END)
            self.backend_frame()
            self.module_sender.send_q(self.frame.id_list, self.frame.brs_list, self.frame.payload_list, self.frame.fd_list)
            if self.que_loop_var.get() == 1:
                self.active_loop_var = True
                    
        else:
            self.initial_interface_state()
            self.error_listbox.insert(END,"Error: CAN is DOWN")
            self.error_listbox.itemconfig(END, {'fg': 'red'})


class SplashScreen:
    def __init__(self, parent):
        self.parent = parent

        self.logo_image = Image.open(r"/home/raspberry/CAN-Tester/images/photo.png").resize((500, 250), Image.ANTIALIAS)
        self.logo_animation = ImageTk.PhotoImage(self.logo_image)

        self.parent.overrideredirect(True)

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        logo_width = self.logo_animation.width()
        logo_height = self.logo_animation.height()
        x = (screen_width - logo_width) // 2
        y = (screen_height - logo_height) // 2
        self.parent.geometry("+{}+{}".format(x, y))

        self.logo_frame = Frame(self.parent)
        self.logo_frame.grid(row=0, column=0, sticky='nsew')

        frame = Frame(self.parent)
        frame.grid(row=1, column=0, sticky='nsew')

        self.logo_label = Label(self.logo_frame, image=self.logo_animation)
        self.logo_label.grid(row=0, column=0)

        self.progressbar = Progressbar(frame, orient='horizontal', length=200)
        self.progressbar.config()
        self.progressbar.grid(row=0, column=0, padx=5)

        self.text_label = Label(frame, text="...", font=("Arial", 11))
        self.text_label.grid(row=0, column=1, padx=(200,0), sticky='e')

        self.list = ['.modules', 'CAN-HAT.sh' , 'continue', '.install','initialize','continue']

        self.parent.update()

    def config_splash(self):
        self.text_label.config(text = random.choice(self.list))

    def destroy(self):
        self.parent.overrideredirect(False)
        self.parent.destroy()

