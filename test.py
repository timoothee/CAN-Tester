import tkinter  as tk 
from tkinter import *

root = Tk("")

def callback(x):
    print(x)

y= 77

button = Button(root, text="Press", command=callback(y))
button.grid()

root.mainloop()