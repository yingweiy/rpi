import RPi.GPIO as GPIO
import time

def init():
    IRPin = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IRPin, GPIO.IN)

def loopCheck():
    while True:
        d = GPIO.input(IRPin)
        print(d)
        time.sleep(0.1)

def OnHit():
    return GPIO.input(IRPin)


