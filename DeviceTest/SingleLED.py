import RPi.GPIO as GPIO
from espeak import espeak
import time
from random import randint

print 'Controlling LED test'
led_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
espeak.set_parameter(espeak.Parameter.Rate, 130)
espeak.set_parameter(espeak.Parameter.Pitch, 60)

try:
    while 1:
        print ("turn on led")
        espeak.synth("The light is on")
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(randint(3,10))
        print("turn off led")
        espeak.synth("The light is off")
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(5)

except KeyboardInterrupt:
    GPIO.output(led_pin, GPIO.LOW)
    GPIO.cleanup()

print 'done.'


