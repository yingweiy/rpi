import sys, tty, termios, os
import device.L298NHBridge as car
import time
import device.CameraServo as cs
import subprocess
import device.IR as IR
import random

def speak(s):
	os.system("espeak -s 100 '" + s +"'")

def take_command_map(cmd_id):
    global live, speed, neck
    
    # The car will drive reverse when the "s" key is pressed
    if (cmd_id == 1):
        car.drive(1, 1)

    # The car will forward when the "w" key is pressed
    if (cmd_id == 2):
        car.drive(-1, -1)

    # Stop the motors
    if (cmd_id == 3):
        car.stop()

    # The "d" key will toggle the steering right
    if (cmd_id == 4):
        car.turn(dir=-1)

    # The "a" key will toggle the steering left
    if (cmd_id == 5):
        car.turn(dir=1)

    if (cmd_id == 6):
        car.turn(dir=1)
        time.sleep(0.2)
        car.stop()

    if (cmd_id == 7):
        car.turn(dir=-1)
        time.sleep(0.2)
        car.stop()

    if (cmd_id == 8):
        neck.look_left()

    if (cmd_id == 9):
        neck.look_right()

    if (cmd_id == 10):
        neck.look_up()

    if (cmd_id == 11):
        neck.look_down()

    # The "x" key will break the loop and exit the program
    if (cmd_id == 0):
        car.stop()
        car.exit()
        live = False

def avoidObstacle():
    print('Obstacle detected. Avoidance process started...')
    car.drive(1, 1)
    time.sleep(0.5)
    car.turn(dir=-1)
    time.sleep(0.2)
    car.drive(-1, -1)

def perception():
    OnHit = IR.OnHit()
    if OnHit:
        avoidObstacle()

def process():
    pass

def decision():
    pass

def action():
    cmd_id = random.randint(1,11)
    take_command_map(cmd_id)
    time.sleep(0.5)

def init():    
    IR.init()

def cleanup():
    global cam_process
    print('Cleaning up...')
    print('kill -9 ' + str(cam_process.pid))
    os.system('kill -9 '+str(cam_process.pid))
    print("Program Ended")

def main():
    global neck, cam_process, nc_process, command_queue
    command_queue = []
    init()    
    live=True
    neck = cs.CameraServo()
    last_ip=input('Server IP 192.168.1.?? (default to Mac 27@24)')
    if len(last_ip)<1:
        last_ip = '24'
    ip = '192.168.1.' + str(last_ip)
    print('Server IP:', ip)

    # os.system('raspivid -o - -t 0 -w 800 -h 600 -fps 24 | nc ' + ip + ' 2222')
    cam_process = subprocess.Popen('raspivid -o - -t 0 -w 800 -h 600 -fps 24 > ~/cam_pipe &', shell=True)
    nc_process = subprocess.Popen('nc ' + ip + ' 2222 < ~/cam_pipe &', shell=True)

    while live:
        perception()
        process()
        decision()
        action()

    cleanup()


if __name__ == "__main__":
    main()





