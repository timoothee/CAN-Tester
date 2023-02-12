import tkinter as tk
from tkinter import *
import os
import sys
from tkinter import messagebox

root = Tk()

slider = Scale(root, from_=0, to= 100, length=100, resolution=1, orient=VERTICAL)
slider.grid()

root.mainloop()