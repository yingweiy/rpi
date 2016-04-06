import RPi.GPIO as GPIO

class CameraServo:
    def __init__(self):
        pin_pan=18
        pin_tilt=19
        pan_range=[80, 100]
        tilt_range=[0,80]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_pan, GPIO.OUT)
        GPIO.setup(pin_tilt, GPIO.OUT)
        pwm_pan = GPIO.PWM(pin_pan,50)
        pwm_tilt = GPIO.PWM(pin_tilt, 50)

        pan_degree = 90
        tilt_degree = 40

        pwm_pan.start(self.ConvertDegree2DutyCycle(90))
        pwm_tilt.start(self.ConvertDegree2DutyCycle(40))

    def ConvertDegree2DutyCycle(self, degree):
        return float(degree) / 18.0 + 2.5

    def update_pan(self, angle):
        if angle<self.pan_range[0] or angle>self.pan_range[1]:
            print('Error: out of pan angle boundary.', angle)
            return
        self.pan_degree = angle
        self.pwm_pan.ChangeDutyCycle(self.ConvertDegree2DutyCycle(angle))


    def update_tilt(self, angle):
        if angle < self.tilt_range[0] or angle > self.tilt_range[1]:
            print('Error: out of tilt angle boundary.', angle)
            return
        self.tilt_degree = angle
        self.pwm_tilt.ChangeDutyCycle(self.ConvertDegree2DutyCycle(angle))

    def exit(self):
        self.pwm_pan.stop()
        self.pwm_tilt.stop()

    def look_left(self):
        self.update_pan(self.pan_degree - 5)

    def look_right(self):
        self.update_pan(self.pan_degree + 5)

    def look_up(self):
        self.update_pan(self.tilt_degree - 1)

    def look_down(self):
        self.update_pan(self.tilt_degree + 1)
