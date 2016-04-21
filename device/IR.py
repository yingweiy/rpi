import RPi.GPIO as GPIO
import time

def init():
    global IRPin
    IRPin = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IRPin, GPIO.IN)

def loopCheck():
    global IRPin
    while True:
        d = GPIO.input(IRPin)
        print(d)
        time.sleep(0.1)

def OnHit():
    global IRPin
    return GPIO.input(IRPin)


