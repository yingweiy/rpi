import RPi.GPIO as GPIO
import time

IRPin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(IRPin, GPIO.IN)

while True:
    d = GPIO.input(IRPin)
    print(d)
    time.sleep(0.1)


