import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685

class CameraServo:  #the old one on board
    def __init__(self):
        self.ch_pan = 0
        self.ch_tilt = 1
        self.pan_range=[-70, 100]
        self.tilt_range=[-200, -60]
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

        self.pwm.set_pwm(self.ch_pan, 0, 375)
        self.pwm.set_pwm(self.ch_tilt, 0, 375)

        self.pan_degree = 30
        self.tilt_degree = -130

    def setChannelDegree(self, ch, degree):
        self.pwm.set_pwm(ch, 0, int(degree*1.25+375))

    def center_pan(self):
        self.update_pan(30)

    def center_tilt(self):
        self.update_tilt(-130)

    def update_pan(self, angle):
        if angle<self.pan_range[0] or angle>self.pan_range[1]:
            return
        self.pan_degree = angle
        self.setChannelDegree(self.ch_pan, angle)

    def update_tilt(self, angle):
        if angle < self.tilt_range[0] or angle > self.tilt_range[1]:
            return
        self.tilt_degree = angle
        self.setChannelDegree(self.ch_tilt, angle)

    def exit(self):
        pass

    def look_right(self):
        self.update_pan(self.pan_degree - 5)

    def look_left(self):
        self.update_pan(self.pan_degree + 5)

    def look_down(self):
        self.update_tilt(self.tilt_degree - 5)

    def look_up(self):
        self.update_tilt(self.tilt_degree + 5)



class CameraServo0:  #the old one on board
    def __init__(self):
        self.pin_pan=18
        self.pin_tilt=19
        self.pan_range=[60, 120]
        self.tilt_range=[0, 80]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_pan, GPIO.OUT)
        GPIO.setup(self.pin_tilt, GPIO.OUT)
        self.pwm_pan = GPIO.PWM(self.pin_pan,50)
        self.pwm_tilt = GPIO.PWM(self.pin_tilt, 50)
        self.pan_degree = 90
        self.tilt_degree = 10

        self.pwm_pan.start(self.ConvertDegree2DutyCycle(90))
        self.pwm_tilt.start(self.ConvertDegree2DutyCycle(10))

    def ConvertDegree2DutyCycle(self, degree):
        return float(degree) / 18.0 + 2.5

    def center_pan(self):
        self.update_pan(90)

    def center_tilt(self):
        self.update_tilt(10)

    def update_pan(self, angle):
        if angle<self.pan_range[0] or angle>self.pan_range[1]:
            return
        self.pan_degree = angle
        self.pwm_pan.ChangeDutyCycle(self.ConvertDegree2DutyCycle(angle))


    def update_tilt(self, angle):
        if angle < self.tilt_range[0] or angle > self.tilt_range[1]:
            return
        self.tilt_degree = angle
        self.pwm_tilt.ChangeDutyCycle(self.ConvertDegree2DutyCycle(angle))

    def exit(self):
        self.pwm_pan.stop()
        self.pwm_tilt.stop()

    def look_right(self):
        self.update_pan(self.pan_degree - 5)

    def look_left(self):
        self.update_pan(self.pan_degree + 5)

    def look_down(self):
        self.update_tilt(self.tilt_degree - 5)

    def look_up(self):
        self.update_tilt(self.tilt_degree + 5)
