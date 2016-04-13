import RPi.GPIO as GPIO
import time

IRPin = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IRPin, GPIO.IN)

while True:
    d = GPIO.input(IRPin)
    if d==0:
        print 'Obstacle detected'
        time.sleep(0.1)
