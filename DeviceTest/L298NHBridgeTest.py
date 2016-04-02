import sys, tty, termios, os
import L298NHBridge as HBridge
import time

speed = 0.5

# Instructions for when the user has an interface
print("w/s: direction")
print("a/d: steering")
print("q: stops the motors")
print("p: print motor speed (L/R)")
print("x: exit")

# The catch method can determine which key has been pressed
# by the user on the keyboard.
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

# Infinite loop
# The loop will not end until the user presses the
# exit key 'X' or the program crashes...

def printscreen():
	# Print the motor speed just for interest
	os.system('clear')
	print("w/s: direction")
	print("a/d: steering")
	print("q: stops the motors")
	print("x: exit")
	print("========== Speed Control ==========")
	print("speed:  ", speed)

def turn(dir):
    global speed
    drive(-dir, dir)

def stop():
	HBridge.setMotorLeft(0)
	HBridge.setMotorRight(0)

def drive(left_dir, right_dir):
	global speed
	HBridge.setMotorLeft(left_dir*speed)
	HBridge.setMotorRight(right_dir*speed)
	printscreen()

while True:
	# Keyboard character retrieval method. This method will save
	# the pressed key into the variable char
	char = getch()

	# The car will drive forward when the "w" key is pressed
	if(char == "s"):
		drive(1, 1)

	# The car will reverse when the "s" key is pressed
	if(char == "w"):
		drive(-1, -1)

	# Stop the motors
	if(char == "q"):
		stop()
		printscreen()

	# The "d" key will toggle the steering right
	if(char == "d"):
		turn(dir=-1)

	# The "a" key will toggle the steering left
	if(char == "a"):
		turn(dir=1)

	if (char==','):
		turn(dir=-1)
		time.sleep(0.1)
		stop()

	if (char=='.'):
		turn(dir=1)
		time.sleep(0.1)
		stop()

	if (char=='1'):
		speed=0.1

	if (char=='2'):
		speed=0.5

	if (char=='3'):
		speed=1.0

	# The "x" key will break the loop and exit the program
	if(char == "x"):
		stop()
		HBridge.exit()
		print("Program Ended")
		break
	
	# The keyboard character variable char has to be set blank. We need
	# to set it blank to save the next key pressed by the user
	char = ""
# End
