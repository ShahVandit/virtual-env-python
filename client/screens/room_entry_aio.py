import aiohttp
import asyncio
from threading import Thread
from avatar_selection import AvatarSelectionScreen

async def join_room_async(room_name):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:8080/join_room'  # Adjust as needed
        data = {'room_name': room_name}
        async with session.post(url, json=data) as resp:
            response = await resp.json()
            return {"status_code": resp.status, "message": response}

def run_asyncio_coroutine(coroutine, callback):
    """
    Runs the given coroutine in a separate thread, calling `callback` with its result when done.
    """
    def run_and_callback():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coroutine)
        callback(result)
    
    Thread(target=run_and_callback).start()

# Example callback function
def on_join_room_response(result):
    print("Join room response:", result)
    if result['status_code'] == 200:  # Assuming 200 means success
        room_name = result['message']['room_name']
        session_id = result['message']['session_id']
        # Assuming current_screen is accessible and has the set_room_details method
        current_screen = AvatarSelectionScreen(screen, room_name,session_id)
        # Proceed with showing or updating the current screen as necessary
    else:
        # Handle error or unsuccessful attempt to join room
        print("Failed to join room:", result['message'])
