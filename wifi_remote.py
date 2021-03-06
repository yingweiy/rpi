import sys, tty, termios, os
import device.L298NHBridge as car
import time
import device.CameraServo as cs
import subprocess
import device.Relay as relay
import device.HCSR04 as sonar
import device.Button as button

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
	os.system("espeak -s 100 '" + s +"'")

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
    print("n: distance measure")
    print("x: exit")

def take_command_map():
    global live, speed, neck, car, switch, Sonar
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
        car.drive(1,1)
        time.sleep(0.1)
        car.stop()

    if (char == '.'):
        car.turn(dir=-1)
        time.sleep(0.1)
        car.stop()
        car.drive(1, 1)
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

    if (char == 'n'):
        print('Distance to front object is :', Sonar.measure(), ' cm.')

    # The "x" key will break the loop and exit the program
    if (char == "x"):
        car.stop()
        car.exit()
        switch.off()
        live = False

def process():
    pass

def perception():
    if nose.is_pressed():
       print('Oh, no~ Hit on something!')
       car.stop()
       time.sleep(0.5)
       print('Go back...')
       car.drive(1,1)

def decision():
    pass

def action():
    take_command_map()


def cleanup():
    print('Cleaning up...')
    print('kill -9 ' + str(cam_process.pid))
    os.system('kill -9 '+str(cam_process.pid))
    print("Program Ended")

printscreen()
live=True
neck = cs.CameraServo()
neck.center_pan()
neck.center_tilt()
Sonar = sonar.HCSR()
nose = button.Button()

last_ip=input('Server IP 192.168.1.?? (default to Mac 27@24)')
if len(last_ip)<1:
    last_ip = '24'
ip = '192.168.1.' + str(last_ip)
print('Server IP:', ip)

# os.system('raspivid -o - -t 0 -w 800 -h 600 -fps 24 | nc ' + ip + ' 2222')
cam_process = subprocess.Popen('raspivid -o - -t 0 -w 800 -h 600 -fps 24 > ~/cam_pipe &', shell=True)
nc_process = subprocess.Popen('nc ' + ip + ' 2222 < ~/cam_pipe &', shell=True)

switch = relay.Relay()
switch.on()

while live:
    perception()
    process()
    decision()
    action()

cleanup()




