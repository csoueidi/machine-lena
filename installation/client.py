import asyncio
import websockets
import json

# Global variable for the controller Pi's IP address
CONTROLLER_PI_IP = "172.20.10.2"  # Replace with the actual IP address
CONTROLLER_PI_PORT = "8765"
CONTROLLER_PI_URI = f"ws://{CONTROLLER_PI_IP}:{CONTROLLER_PI_PORT}"

async def get_choreographies():
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'getAllChoreographies'}))
        response = await websocket.recv()
        print(f"Choreographies: {response}")

async def is_executing():
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'isExecuting'}))
        response = await websocket.recv()
        print(f"Is Executing: {response}")

async def execute_choreography(name):
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'execute', 'choreographyName': name}))
        response = await websocket.recv()
        print(f"Response: {response}")

# Example usage
asyncio.get_event_loop().run_until_complete(get_choreographies())
asyncio.get_event_loop().run_until_complete(is_executing())
asyncio.get_event_loop().run_until_complete(execute_choreography("Choreography1"))
