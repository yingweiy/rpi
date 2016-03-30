import time
import picamera
import picamera.array

with picamera.PiCamera() as cam:
    with picamera.array.PiRGBArray(cam) as stream:
        cam.resolution=(1024, 768)
        cam.start_preview()
        time.sleep(2)
        cam.capture(stream, 'rgb')
        print(stream.array.shape)

