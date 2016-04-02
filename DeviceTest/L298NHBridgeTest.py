import sys, tty, termios, os
import L298NHBridge as HBridge

speedleft = 0
speedright = 0

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
	print("left motor:  ", speedleft)
	print("right motor: ", speedright)

def drive(delta_left, delta_right):
	# synchronize after a turning the motor speed
	if speedleft != speedright:
		speedleft = speedright

	# accelerate the RaPi car
	speedleft = speedleft + delta_left
	speedright = speedright + delta_right

	if speedleft > 1:
		speedleft = 1
	if speedright > 1:
		speedright = 1

	HBridge.setMotorLeft(speedleft)
	HBridge.setMotorRight(speedright)
	printscreen()

while True:
    # Keyboard character retrieval method. This method will save
    # the pressed key into the variable char
	char = getch()


	# The car will drive forward when the "w" key is pressed
	if(char == "w"):
		drive(0.1, 0.1)

    # The car will reverse when the "s" key is pressed
	if(char == "s"):
		drive(-0.1, -0.1)

    # Stop the motors
	if(char == "q"):
		speedleft = 0
		speedright = 0
		HBridge.setMotorLeft(speedleft)
		HBridge.setMotorRight(speedright)
		printscreen()

    # The "d" key will toggle the steering right
	if(char == "d"):		
		drive(0.1, -0.1)

    # The "a" key will toggle the steering left
	if(char == "a"):
		drive(-0.1, 0.1)

	# The "x" key will break the loop and exit the program
	if(char == "x"):
		HBridge.setMotorLeft(0)
		HBridge.setMotorRight(0)
		HBridge.exit()
		print("Program Ended")
		break
	
    # The keyboard character variable char has to be set blank. We need
	# to set it blank to save the next key pressed by the user
	char = ""
# End
