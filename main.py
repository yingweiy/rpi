import sys, tty, termios, os
import device.L298NHBridge as car
import time
import device.CameraServo as cs
import device.CameraRPi as cam

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
    print("j/l: pan camera")
    print("c: center camera")
    print("i/k: tilt camera")
    print("1/2/3: speed shift")
    print("q: stops the motors")
    print("m: speak muffin")
    print("x: exit")

def take_command_map():
    global live, speed
    char = getch()

    if (char == 'm'):
        speak("Muffin")

    if (char == 'h'):
        speak("Hello")

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

    if (char == 'j'):
        neck.look_left()

    if (char == 'l'):
        neck.look_right()

    if (char == 'i'):
        neck.look_up()

    if (char == 'k'):
        neck.look_down()

    if (char == 'c'):
        neck.center_pan()
        neck.center_tilt()

    # The "x" key will break the loop and exit the program
    if (char == "x"):
        car.stop()
        car.exit()
        print("Program Ended")
        live = False

def perception():
    eye.capture()

def process():
    pass

def decision():
    pass

def action():
    take_command_map()

printscreen()
live=True
neck = cs.CameraServo()
ip=input('Server IP: (default to 192.168.1.24)')
if len(ip)<3:
    ip = '192.168.1.24'
eye = cam.CameraRPi(server_ip=ip)

for foo in eye.camera.capture_continuous(eye.stream, 'raw'):
    if not live:
        break

    perception()
    process()
    decision()
    action()




