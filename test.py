import RPi.GPIO as GPIO
import time


gpio = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup(gpio):
    GPIO.setup(gpio,GPIO.OUT)
    GPIO.output(gpio,GPIO.LOW)

setup(gpio)

GPIO.output(gpio,GPIO.HIGH)
GPIO.output(gpio,GPIO.LOW)