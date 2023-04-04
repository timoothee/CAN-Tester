import PySimpleGUI as sg
import time
import threading
class SplashScreen:

    def threadfunc(self):
        t1 = threading.Thread(target=self.splaaaash)
        t1.start()

    def splaaaash(self):
        splash_image = "photo.png"
        layout = [[sg.Image(filename=splash_image, background_color="white", key="-SPLASH-")]]
        splash_window = sg.Window("Pantalla de bienvenida", layout, no_titlebar=True, element_justification="center")

        sg.PopupAnimated(splash_image, background_color="white")

        sg.PopupAnimated(None)

        time.sleep(2)

        splash_window.close()
