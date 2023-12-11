import io
import cv2
import numpy as np
import socketserver
import threading
from threading import Condition
import time
from http import server
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# HTML for the web page
PAGE = """\
<html>
<head>
<title>PiCamera2 MJPEG Streaming Demo</title>
</head>
<body>
<h1>PiCamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="1280" height="720" />
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
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
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Initialize PiCamera2 for video capture
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "XRGB8888"})
picam2.configure(video_config)
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))
picam2.start()

# Load the MobileNet SSD model
config_file = '/home/pi/projects/machine-lena/camera/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = '/home/pi/projects/machine-lena/camera/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Configure model
model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

prev_frame = None

def streaming_server():
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        picam2.stop_recording()

# Start the streaming server in a separate thread
streaming_thread = threading.Thread(target=streaming_server)
streaming_thread.start()

try:
    while True:
        time.sleep(0.1)
        frame = picam2.capture_array()

        # Convert frame from XRGB to BGR for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect people in the frame
        classIds, confs, bbox = model.detect(frame, confThreshold=0.5)
        people_count = sum([1 for classId in classIds if classId == 1])  # Class 1 is for people in COCO dataset

        # Motion detection
        if prev_frame is not None:
            frame_delta = cv2.absdiff(prev_frame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            motion_level = np.sum(thresh) / (frame.shape[0] * frame.shape[1])

            if motion_level > 5:  # Motion threshold
                if motion_level > 30:
                    motion_speed = 'Fast'
                elif motion_level > 15:
                    motion_speed = 'Medium'
                else:
                    motion_speed = 'Slow'
                print(f"People count: {people_count}, Motion: {motion_speed}")

        prev_frame = gray

        # Convert frame to JPEG format for streaming
        _, jpeg_frame = cv2.imencode('.jpg', frame)
        with output.condition:
            output.frame = jpeg_frame.tobytes()
            output.condition.notify_all()

        # Show the frame
        # cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    streaming_thread.join()  # Ensure the streaming thread is cleanly stopped
