# Camera web streaming example

import io
import picamera
import logging
import socketserver
from threading import Condition
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



def GetUrl() -> str:
    deviceIpAddr = str(subprocess.check_output("hostname -I", shell=True))
    deviceIpAddr = deviceIpAddr[2:]
    deviceIpAddr = deviceIpAddr[:-4]
    return "http://"+ str(deviceIpAddr) +":"+ str(HTTP_PORT) +"/"




def Start():
    global videoOutput
    global server
    global camera
    camera = picamera.PiCamera(resolution=VIDEO_RESOLUTION, framerate=VIDEO_FRAME_RATE)
    videoOutput = StreamingOutput()
    camera.rotation = VIDEO_SCREEN_ROTATED
    camera.start_recording(videoOutput, format='mjpeg')
    try:
        address = ('', HTTP_PORT)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
        print("Camera Streamer Stopped")
    finally:
        camera.stop_recording()

            
def Stop():
    global server
    global camera
    camera.stop_recording()
    server.shutdown()
    server.server_close()
    