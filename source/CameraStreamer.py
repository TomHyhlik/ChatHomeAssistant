# Camera web streaming example

import io
import picamera
import logging
import socketserver
from threading import Condition
import threading
from http import server
import subprocess

VIDEO_RESOLUTION = '1920x1080'
VIDEO_FRAME_RATE = 30
VIDEO_SCREEN_ROTATED = 180

HTTP_PORT = 8000

PAGE="""\
<html>
<head>
<title>Camera Streamer</title>
</head>
<body>
<center><h1>Camera Streamer</h1></center>
<center><img src="stream.mjpg" width="1920" height="1080"></center>
</body>
</html>
"""



class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        global videoOutput
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with videoOutput.condition:
                        videoOutput.condition.wait()
                        frame = videoOutput.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class CameraStreamer:
    def __init__(self):
        self.__cameraInitialized = False
        self.camera = None
        self.server = None
        self.server_thread = None

    def get_url(self) -> str:
        """
        Get http url by which the streamed video is accessed
        """
        deviceIpAddr = str(subprocess.check_output("hostname -I", shell=True))
        deviceIpAddr = deviceIpAddr[2:]
        deviceIpAddr = deviceIpAddr[:-4]
        return f"http://{deviceIpAddr}:{HTTP_PORT}/"

    def init_camera(self):
        """
        Initialize the camera
        """
        global videoOutput
        if not self.__cameraInitialized:
            self.camera = picamera.PiCamera(resolution=VIDEO_RESOLUTION, framerate=VIDEO_FRAME_RATE)
            videoOutput = StreamingOutput()
            self.camera.rotation = VIDEO_SCREEN_ROTATED
            self.__cameraInitialized = True
        self.camera.start_recording(videoOutput, format='mjpeg')

    def start_server(self):
        """
        Start video streaming server in thread
        """
        print("Starting server")
        address = ('', HTTP_PORT)
        self.server = StreamingServer(address, StreamingHandler)
        self.server.serve_forever()

    def start(self):
        """
        Start video streaming server
        """
        self.init_camera()
        try:
            self.server_thread = threading.Thread(target=self.start_server)
            self.server_thread.start()
        except Exception as e:
            print("ERROR: Failed to start video streaming server:", e)
                
    def stop(self):
        """
        Stop video streaming server
        """
        if self.camera:
            self.camera.stop_recording()
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.server_thread:
            self.server_thread.join()