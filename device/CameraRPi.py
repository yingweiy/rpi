import io
import socket
import struct
import time
import picamera

class CameraRPi:
    def __init__(self, server_ip = '192.168.1.24'):
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        self.client_socket = socket.socket()
        self.client_socket.connect((server_ip, 8000))
        # Make a file-like object out of the connection
        self.connection = self.client_socket.makefile('wb')
        self.camera = picamera.PiCamera()

    def capture(self):
        try:
            self.camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            self.camera.start_preview()
            time.sleep(2)
            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in self.camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                self.connection.write(struct.pack('<L', stream.tell()))
                self.connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                self.connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                if time.time() - start > 1000:
                    break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            # Write a length of zero to the stream to signal we're done
            self.connection.write(struct.pack('<L', 0))
        except:
            print('Camera server is lost.')

    def exit(self):
        self.connection.close()
        self.client_socket.close()

