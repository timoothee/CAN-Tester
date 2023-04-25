import RPi.GPIO as GPIO
import time


class rgb_fade():
    def __init__(self):
        self.gpio = 4
        self.modify = 2500
        self.add = 0.01
        self.add_1 = 0.001
        self.add_2 = 0.01
        self.delay = 1/self.modify

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpio,GPIO.OUT)
        GPIO.output(self.gpio,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(self.gpio,GPIO.HIGH)
        time.sleep(1)


    def fade_out(self):
        for i in range(int(self.modify/100)):

            GPIO.output(self.gpio,GPIO.LOW)
            time.sleep(self.add_2 - self.delay)
            GPIO.output(self.gpio,GPIO.HIGH)
            time.sleep(self.add_1 + self.delay)
 
            self.add_2 = self.add_2 - self.delay
            self.add_1 = self.add_1 + self.delay

            print(i, self.add_2, self.add_1)


    def fade_in(self):
        for i in range(int(self.modify/100)):

            GPIO.output(self.gpio,GPIO.LOW)
            time.sleep(self.add_1 + self.delay)
            GPIO.output(self.gpio,GPIO.HIGH)
            time.sleep(self.add_2 - self.delay)

            self.add_2 = self.add_2 - self.delay
            self.add_1 = self.add_1 + self.delay

            print(i, self.add_2, self.add_1)

    def initial_state(self):
        self.add_1 = 0.001
        self.add_2 = 0.01

faiding = rgb_fade()

for i in range(5):
    faiding.fade_out()
    faiding.initial_state()
    time.sleep(1)
    faiding.fade_in()
    faiding.initial_state()



