import RPi.GPIO as GPIO

class CameraServo:
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
        self.tilt_degree = 20

        self.pwm_pan.start(self.ConvertDegree2DutyCycle(90))
        self.pwm_tilt.start(self.ConvertDegree2DutyCycle(20))

    def ConvertDegree2DutyCycle(self, degree):
        return float(degree) / 18.0 + 2.5

    def center_pan(self):
        self.update_pan(90)

    def center_tilt(self):
        self.update_tilt(40)

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
        self.update_tilt(self.tilt_degree - 1)

    def look_up(self):
        self.update_tilt(self.tilt_degree + 1)
