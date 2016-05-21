import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pin = 19
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        return not(GPIO.input(self.pin))


if __name__ == '__main__':
    nose=Button()
    while True:
        if nose.is_pressed():
           print('Button pressed.')
           time.sleep(0.2)
