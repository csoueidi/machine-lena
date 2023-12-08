import cv2
import numpy as np
import sys
import time
from picamera2 import Picamera2

# Initialize PiCamera2 for video capture
# picam2 = Picamera2()
# video_config = picam2.create_video_configuration(main={"format": "XRGB8888"})
# picam2.configure(video_config)
# picam2.start()

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 1080), "format": "XRGB8888"})
picam2.configure(video_config)
picam2.start()


# Load the MobileNet SSD model
config_file = '/home/pi/projects/machine-lena/camera/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = '/home/pi/projects/machine-lena/camera/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Configure model
model.setInputSize(320, 320)
model.setInputScale(1.0/ 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

prev_frame = None

# print("finished setup")

while True:
    time.sleep(0.2)
    frame = picam2.capture_array()

    # Convert frame from XRGB to BGR for OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    # Convert to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    # Detect people in the frame
    classIds, confs, bbox = model.detect(frame, confThreshold=0.5)
    people_count = sum([1 for classId in classIds if classId == 1])  # Class 1 is for people in COCO dataset
    #  print("people_count")
    
    # Motion detection
    if prev_frame is not None:
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_level = np.sum(thresh) / (frame.shape[0] * frame.shape[1])

        if motion_level < 5:  # No motion threshold
            # print("No motion detected")
            x=5
        else:
            if motion_level > 30:
                motion_speed = 'Fast'
            elif motion_level > 15:
                motion_speed = 'Medium'
            else:
                motion_speed = 'Slow'
            print(f"People count: {people_count}, Motion: {motion_speed}")

    prev_frame = gray

    # Show the frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()