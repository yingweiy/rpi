import RPi.GPIO as GPIO
import time

class HCSR:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = 20
		self.ECHO = 21

		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)

		GPIO.output(self.TRIG, False)
		print("Waiting for sensor to settle...")
		time.sleep(1)


	def measure(self):
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)

		while GPIO.input(self.ECHO)==0:
			pulse_start = time.time()

		while GPIO.input(self.ECHO)==1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		return distance



if __name__ ==  "__main__":
	sonar = HCSR()
	while True:
		print("Distance", sonar.measure(), "cm")
		time.sleep(0.5)
	GPIO.cleanup()



