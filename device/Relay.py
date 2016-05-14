import RPi.GPIO as GPIO


class Relay:
    def __init__(self):
        GPIO.setmode(io.BCM)
        self.pin = 8
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)



