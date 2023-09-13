import tkinter as tk
root = tk.Tk()
sw = root.winfo_screenwidth()  # 1080
sh = root.winfo_screenheight()  # 1920
xoff = (sw // 2) - 200
yoff = (sh // 2) - 100
root.geometry(f'400x200+{xoff}+{yoff}')
root.overrideredirect(True)