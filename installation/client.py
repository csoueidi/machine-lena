import asyncio
import websockets
import json

# Global variable for the controller Pi's IP address
CONTROLLER_PI_IP = "172.20.10.11"  # Replace with the actual IP address
CONTROLLER_PI_PORT = "8767"
CONTROLLER_PI_URI = f"ws://{CONTROLLER_PI_IP}:{CONTROLLER_PI_PORT}"

async def get_choreographies():
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'getAllChoreographies'}))
        response = await websocket.recv()
        return json.loads(response)  # Return the list of choreographies



async def is_executing():
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'isExecuting'}))
        response = await websocket.recv()
        return json.loads(response)  # Return the boolean value


async def execute_choreography(name):
    async with websockets.connect(CONTROLLER_PI_URI) as websocket:
        await websocket.send(json.dumps({'action': 'execute', 'choreographyName': name}))
        response = await websocket.recv()
        print(f"Response: {response}")

async def handle_choreographies(state_machine):
    executing = json.loads(await is_executing())
    if executing.get('status') == 'executing':
        return  # Skip if already executing

    choreographies = json.loads(await get_choreographies())
    current_state = state_machine.get_state()

    # Filter choreographies based on the current state
    filtered_choreographies = [choreo for choreo in choreographies if current_state in choreo['tags']]

    if filtered_choreographies:
        # Execute the first choreography from the filtered list
        await execute_choreography(filtered_choreographies[0]['name'])


# Example usage
asyncio.get_event_loop().run_until_complete(get_choreographies())
asyncio.get_event_loop().run_until_complete(is_executing())
asyncio.get_event_loop().run_until_complete(execute_choreography("simple.chor"))
