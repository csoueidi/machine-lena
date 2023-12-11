import sys
from pathlib import Path
import os

import random
import asyncio
import websockets
import json

import time


# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
parent_dir = '/home/pi/demo/code'
sys.path.append(parent_dir)
print(sys.path)

import config.config as config
 

from myparser import MyParser

# Global variable for the port
SERVER_PORT = 8768


is_executing = False
executing_file = None
execution_message = None
 

motors = config.get_motors_map()
myParser = MyParser()

# Define speed ranges based on motion levels
def get_speed_for_motion_level(motion_level):
    # Define your logic here. Example:
    if motion_level == 1:
        return 0.05
    elif motion_level == 2:
        return 0.1
    elif motion_level == 3:
        return 0.5
    elif motion_level == 4:
        return 1
    elif motion_level == 5:
        return 2
    elif motion_level == 6:
        return 50
    else:
        return 0
    
motor_states = {motor_id: {'last_direction': None, 'accumulated_movement': 0} for motor_id in motors.keys()}

def get_target_position(motor_id, current_position):
    min_movement = 0.05
    max_accumulated_movement = 0.6  # 30% movement
    state = motor_states[motor_id]

    # Check if the motor has reached its limits and needs to reverse direction
    if current_position <= 0:
        target_position = current_position + min_movement
        state['last_direction'] = 'increase'
        state['accumulated_movement'] = min_movement
    elif current_position >= 1:
        target_position = current_position - min_movement
        state['last_direction'] = 'decrease'
        state['accumulated_movement'] = min_movement
    else:
        # Continue in the same direction if the accumulated movement is less than x%
        if state['last_direction'] == 'increase' and state['accumulated_movement'] < max_accumulated_movement:
            target_position = min(current_position + min_movement, 1)
            state['accumulated_movement'] += min_movement
        elif state['last_direction'] == 'decrease' and state['accumulated_movement'] < max_accumulated_movement:
            target_position = max(current_position - min_movement, 0)
            state['accumulated_movement'] += min_movement
        else:
            # Allow changing direction if the motor has moved x% in one direction
            if random.choice([True, False]):
                target_position = min(current_position + min_movement, 1)
                state['last_direction'] = 'increase'
                state['accumulated_movement'] = min_movement
            else:
                target_position = max(current_position - min_movement, 0)
                state['last_direction'] = 'decrease'
                state['accumulated_movement'] = min_movement

    return target_position



async def handler(websocket, path):

    global is_executing, executing_file, execution_message, myParser, motors
    
    async for message in websocket:
        data = json.loads(message)

        if data['action'] == 'getAllChoreographies':
            files = [f for f in os.listdir('chors') if f.endswith('.chor')]
            sorted_files = sorted(files)
            await websocket.send(json.dumps(sorted_files))

        elif data['action'] == 'isExecuting':
            await websocket.send(json.dumps({"is_executing": is_executing, "message": execution_message}))

        elif data['action'] == 'execute':
            filename = data['choreographyName']
            if is_executing:
                is_executing = True
                execution_message= "Another choreography is being executed"
            file_path = os.path.join(os.getcwd(), 'chors', filename)
            if file_path.endswith('.chor') and os.path.exists(file_path):
        
        
                is_executing = True    
                execution_message = myParser.execute(file_path, filename)
                is_executing = False
          

            await websocket.send(json.dumps({"is_executing": is_executing, "message": execution_message}))
      
        elif data['action'] == 'move':
            motion_level = data['motion_level']
            speed = get_speed_for_motion_level(motion_level)

            # Randomly select one or more motors
            selected_motor_ids = random.sample(list(motors.keys()), random.randint(1, len(motors)))

            for motor_id in selected_motor_ids:
                motor = motors.get(int(motor_id))
                if motor:
                    current_position = motor.get_position()  # Assuming you have a method to get the current position
                    target_position = get_target_position(motor_id, current_position)
                    motor.move(target_position, speed)

            await websocket.send(json.dumps({"status": "Motors moved"}))



 
start_server = websockets.serve(handler, "0.0.0.0", SERVER_PORT)
print("Running controller websockets")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
