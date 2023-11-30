import cv2
import numpy as np
import sys
import time

# Check if in testing mode
testing = '--testing' in sys.argv

# Initialize camera
camera_port = 0 if testing else 'YOUR_RASPBERRY_PI_CAMERA_PORT'
cap = cv2.VideoCapture(camera_port)

# Load the MobileNet SSD model
config_file = '/Users/chukrisoueidi/Src/lena/machine/machine-lena/camera/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = '/Users/chukrisoueidi/Src/lena/machine/machine-lena/camera/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

# Configure model
model.setInputSize(320, 320)
model.setInputScale(1.0/ 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

prev_frame = None

while True:
    time.sleep(0.1)
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect people in the frame
    classIds, confs, bbox = model.detect(frame, confThreshold=0.5)
    people_count = sum([1 for classId in classIds if classId == 1])  # Class 1 is for people in COCO dataset

    # Motion detection
    if prev_frame is not None:
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_level = np.sum(thresh) / (frame.shape[0] * frame.shape[1])  # Normalize motion level

        if motion_level < 5:  # No motion threshold
            print("No motion detected")
        else:
            # Classify motion speed
            if motion_level >30:
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

cap.release()
cv2.destroyAllWindows()
