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
    global live
    
    # The car will drive reverse when the "s" key is pressed
    if (cmd_id >0 and cmd_id<=3):
        car.drive(-1, -1)
        time.sleep(random.random()+0.5)

    # The "d" key will toggle the steering right
    if (cmd_id == 4):
        car.turn(dir=-1)
        time.sleep(random.random())

    # The "a" key will toggle the steering left
    if (cmd_id == 5):
        car.turn(dir=1)
        time.sleep(random.random())

    if (cmd_id == 6):
        car.turn(dir=1)
        time.sleep(random.random()*0.5)
        car.stop()

    if (cmd_id == 7):
        car.turn(dir=-1)
        time.sleep(random.random()*0.5)
        car.stop()

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
    time.sleep(random.random()*2+0.5)

def perception():
    OnHit = IR.OnHit()
    if OnHit:
        avoidObstacle()

def process():
    pass

def decision():
    pass

def action():
    cmd_id = random.randint(1,7)
    take_command_map(cmd_id)

def init():
    global neck
    IR.init()
    neck.center_pan()
    neck.center_tilt()
    neck.exit()

def cleanup():
    global cam_process, neck
    neck.exit()
    print('Cleaning up...')
    print('kill -9 ' + str(cam_process.pid))
    os.system('kill -9 '+str(cam_process.pid))
    print("Program Ended")

def main():
    global neck, cam_process, nc_process, command_queue
    command_queue = []
    live=True
    neck = cs.CameraServo()

    last_ip=input('Server IP 192.168.1.?? (default to Mac 27@24)')
    if len(last_ip)<1:
        last_ip = '24'
    ip = '192.168.1.' + str(last_ip)
    print('Server IP:', ip)

    init()
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





