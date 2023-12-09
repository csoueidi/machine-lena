import cv2
import numpy as np
import time
from picamera2 import Picamera2
from collections import deque
import asyncio
import websockets
import json
import random


motion_ranges = [2, 3, 4, 5, 6, 8, 9]   

# Motion Detection and State Machine Code
class MotionStateMachine:
    def __init__(self, motion_ranges):
        self.state = 0
        self.motion_ranges = motion_ranges

    def update(self, motion_level):
        if motion_level < 1:
            self.state = 0
        elif motion_level < 2:
            self.state = 1
        elif motion_level < 5:
            self.state = 2
        elif motion_level < 10:
            self.state = 3
        elif motion_level < 20:
            self.state = 4
        elif motion_level < 30:
            self.state = 5
        else:
            self.state = 6
        return self.state

    def get_state(self):
        return self.state

# Choreography Handling Code
CONTROLLER_PI_IP = "172.20.10.11"  # Replace with the actual IP address
CONTROLLER_PI_PORT = "8768"
CONTROLLER_PI_URI = f"ws://{CONTROLLER_PI_IP}:{CONTROLLER_PI_PORT}"

async def get_choreographies():
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'getAllChoreographies'}))
        response = await websocket.recv()
        return json.loads(response)

async def is_executing():
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'isExecuting'}))
        response = await websocket.recv()
        data = json.loads(response)
        return data['is_executing']  # Extract the is_executing value


async def execute_choreography(name):
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'execute', 'choreographyName': name}))
        response = await websocket.recv()
        # print(f"Response: {response}")

async def handle_choreographies_async(state_machine):
    if await is_executing():
        print(f"is_executing")
        return  # Skip if already executing

    choreographies = await get_choreographies()
    # print(f"Choreos: {choreographies}")

    current_state = state_machine.get_state()

    # Filter choreographies based on the current state substring
    filtered_choreographies = [choreo for choreo in choreographies if current_state in choreo]

    # print(f"Current State: {current_state}")
    # print(f"Filtered Choreographies: {filtered_choreographies}")

    if filtered_choreographies:
        # Select a random choreography from the filtered list
        selected_choreography = random.choice(filtered_choreographies)
        print(f"Selected choreography {selected_choreography}")
        await execute_choreography(selected_choreography)

def handle_choreographies(state_machine):
    asyncio.run(handle_choreographies_async(state_machine))

def handle_move(state_machine):
    asyncio.run(handle_move_async(state_machine))

async def handle_move_async(state_machine):    
    if await is_executing():
        print(f"is_executing")
        return  # Skip if already executing

    

    current_state = state_machine.get_state()
    if current_state > 0 :
        await execute_move(current_state)
 
       


async def execute_move(mlevel):
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'move', 'motion_level': mlevel}))
        response = await websocket.recv()
        # print(f"Response: {response}")        


# Initialize camera and motion detection
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
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

prev_frame = None
motion_history = deque(maxlen=5)

motion_state_machine = MotionStateMachine(motion_ranges)

 


try:
    while True: 
        # time.sleep(0.2)
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

            avg_motion_level = np.mean(motion_history)
            state = motion_state_machine.update(avg_motion_level)

        prev_frame = gray

        print(f" Machine state {motion_state_machine.get_state()}")

        # Handle choreographies based on the current state
        handle_move(motion_state_machine)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    picam2.stop()
    cv2.destroyAllWindows()
