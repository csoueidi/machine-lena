import asyncio
import websockets
import json

# Global variable for the port
SERVER_PORT = 8765

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)

        if data['action'] == 'getAllChoreographies':
            # Replace with your actual logic to get choreographies
            choreographies = ['Choreography1', 'Choreography2', 'Choreography3']
            await websocket.send(json.dumps(choreographies))

        elif data['action'] == 'isExecuting':
            # Replace with your actual logic to check if executing
            is_executing = False
            await websocket.send(json.dumps(is_executing))

        elif data['action'] == 'execute':
            choreography_name = data['choreographyName']
            # Replace with your actual logic to execute the choreography
            print(f"Executing {choreography_name}")
            # Send a confirmation or result back
            await websocket.send(json.dumps({"status": "executing", "choreography": choreography_name}))

start_server = websockets.serve(handler, "0.0.0.0", SERVER_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
