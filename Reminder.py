import tkinter as tk

def change_dropdown(*args):
    print("Selected option: ", var.get())

root = tk.Tk()
root.geometry("500x500")

var = tk.StringVar(root)
var.set("Select an option")

frame = tk.Frame(root)
frame.grid(row= 0, column = 0, sticky="nsew")
frame1 = tk.Frame(root)
frame1.grid(row= 1, column = 1, sticky="nsew")

options = [
    "Option 1",
    "Option 2",
    "Option 3",
    "Option 4",
    "Option 5"
]

dropdown1 = tk.OptionMenu(frame, var, *options, command=change_dropdown)
dropdown1.grid(row = 0, column=0,padx=20)

var2 = tk.StringVar(root)
var2.set("Select an option")

dropdown2 = tk.OptionMenu(frame1, var2, *options, command=change_dropdown)
dropdown2.grid(row = 0, column =0,padx=20)

root.mainloop()
