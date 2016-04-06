import tkinter
import RPi.GPIO as GPIO
import time

pin_pan=18
pin_tilt=19
pan_range=[80, 100]
tilt_range=[0,80]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_pan, GPIO.OUT)
GPIO.setup(pin_tilt, GPIO.OUT)
pwm_pan = GPIO.PWM(pin_pan,50)
pwm_tilt = GPIO.PWM(pin_tilt, 50)

def ConvertDegree2DutyCycle(degree):
    return float(degree) / 18.0 + 2.5

pwm_pan.start(ConvertDegree2DutyCycle(90))
pwm_tilt.start(ConvertDegree2DutyCycle(40))

class App:
    def __init__(self, master):
        frame = tkinter.Frame(master)
        frame.pack()
        scale_pan = tkinter.Scale(frame, from_=70, to=110, orient=tkinter.HORIZONTAL, command=self.update_pan)  #40-100
        scale_tilt = tkinter.Scale(frame, from_=0, to=80, orient=tkinter.HORIZONTAL, command=self.update_tilt)
        scale_pan.grid(row=0)
        scale_tilt.grid(row=1)

    def update_pan(self,angle):
        pwm_pan.ChangeDutyCycle(ConvertDegree2DutyCycle(angle))

    def update_tilt(self, angle):
        pwm_tilt.ChangeDutyCycle(ConvertDegree2DutyCycle(angle))

root = tkinter.Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("200x100+0+0")
root.mainloop()
pwm_pan.stop()
pwm_tilt.stop()
GPIO.cleanup()

