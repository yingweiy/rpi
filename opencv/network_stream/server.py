import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np

# Create the haar cascade
cascPath = "./haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#video_capture = cv2.VideoCapture(0)

def ProcessImage(image):
        open_cv_image = np.array(image)[:, :, ::-1].copy()

        # Display the resulting frame
        cv2.imshow('Video', open_cv_image)
        ApplyFaceDetection = False

        if ApplyFaceDetection:
            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(open_cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            print(len(faces),' faces detected.')

        return 0


# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
                
        if ProcessImage(image)==1:
            break

        image.verify()
        print('Image is verified')
        
finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows()