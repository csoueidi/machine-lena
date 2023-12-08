import cv2
import numpy as np
import time
from picamera2 import Picamera2
from collections import deque

class MotionStateMachine:
    def __init__(self, motion_ranges):
        self.state = 'NoMotion'
        self.motion_ranges = motion_ranges

    def update(self, motion_level):
        if motion_level < self.motion_ranges[0]:
            self.state = 'NoMotion'
         
        elif motion_level < self.motion_ranges[1]:
            self.state = 'VeryLowMotion'
           
        elif motion_level < self.motion_ranges[2]:
            self.state = 'LowMotion'
           
        elif motion_level < self.motion_ranges[3]:
            self.state = 'MediumMotion'
            
        elif motion_level < self.motion_ranges[4]:
            self.state = 'HighMotion'
           
        else:
            self.state = 'VeryHighMotion'
          

        return self.state

    def get_state(self):
        return self.state    

# Initialize camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 1080), "format": "XRGB8888"})
picam2.configure(video_config)
picam2.start()

# Load the MobileNet SSD model
config_file = '/home/pi/projects/machine-lena/installation/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = '/home/pi/projects/machine-lena/installation/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Configure model
model.setInputSize(320, 320)
model.setInputScale(1.0/ 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

prev_frame = None
motion_history = deque(maxlen=5)  # Adjust size for longer history

# Define motion ranges for each level
motion_ranges = [0.01, 1, 3, 5, 10]  # Example values, adjust as needed
motion_state_machine = MotionStateMachine(motion_ranges)

while True:
    time.sleep(0.2)
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    classIds, confs, bbox = model.detect(frame, confThreshold=0.5)
    people_count = sum([1 for classId in classIds if classId == 1])

    if prev_frame is not None:
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_level = np.sum(thresh) / (frame.shape[0] * frame.shape[1])
        motion_history.append(motion_level)

        # Calculate moving average
        avg_motion_level = np.mean(motion_history)

        # Update state machine
        state = motion_state_machine.update(avg_motion_level)
        # print(f"Current State: {state}, People count: {people_count}, Average: {avg_motion_level}")

    prev_frame = gray
    # cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
