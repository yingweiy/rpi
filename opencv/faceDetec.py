import cv2
import picamera
import picamera.array
import time

# Create the haar cascade
cascPath = "./haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#video_capture = cv2.VideoCapture(0)

cam = picamera.PiCamera()
stream = picamera.array.PiRGBArray(cam)
cam.resolution = (1024, 768)
cam.start_preview()
cam.capture(stream, 'rgb')

# Capture frame-by-frame
while True:
    #time.sleep(2)
    frame = stream.array
    print(frame.shape)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    print(len(faces))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cam.stop_preview()
cam.close()
cv2.destroyAllWindows()