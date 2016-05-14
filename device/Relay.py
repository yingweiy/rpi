import RPi.GPIO as GPIO

class Relay:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pin = 8
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)



