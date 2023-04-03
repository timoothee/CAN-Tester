from PIL import Image, ImageTk


class SplashScreen:
    def __init__(self, parent):
        self.parent = parent

        self.logo_image = Image.open("photo.png").resize((500, 250), Image.ANTIALIAS)
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

    def abc(self):
        self.text_label.config(text = random.choice(self.list))

    def destroy(self):
        self.parent.overrideredirect(False)
        self.parent.destroy()
