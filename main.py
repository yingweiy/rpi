import sys, tty, termios, os
import device.L298NHBridge as car
import time

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def speak(s):
	os.system("espeak '" + s +"'")

def printscreen():
    os.system('clear')
    print("w/s: direction")
    print("a/d: turn")
    print("<>: steering")
    print("q: stops the motors")
    print("x: exit")

def take_command_map():
    global live, car, speed
    char = getch()

    if (char == 'm'):
        speak("Muffin")

    # The car will drive forward when the "w" key is pressed
    if (char == "s"):
        car.drive(1, 1)

    # The car will reverse when the "s" key is pressed
    if (char == "w"):
        car.drive(-1, -1)

    # Stop the motors
    if (char == "q"):
        car.stop()
        printscreen()

    # The "d" key will toggle the steering right
    if (char == "d"):
        car.turn(dir=-1)

    # The "a" key will toggle the steering left
    if (char == "a"):
        car.turn(dir=1)

    if (char == ','):
        car.turn(dir=1)
        time.sleep(0.1)
        car.stop()

    if (char == '.'):
        car.turn(dir=-1)
        time.sleep(0.1)
        car.stop()

    if (char == '1'):
        speed = 0.1

    if (char == '2'):
        speed = 0.5

    if (char == '3'):
        speed = 1.0

    # The "x" key will break the loop and exit the program
    if (char == "x"):
        car.stop()
        car.exit()
        print("Program Ended")
        live = False

def perception():
    pass

def process():
    pass

def decision():
    pass

def action():
    take_command_map()

printscreen()
live=True
while live:
    perception()
    process()
    decision()
    action()

