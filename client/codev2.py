import pygame
import sys
from screens.room_entry import RoomEntryScreen
from screens.avatar_selection import AvatarSelectionScreen
from screens.virtual_environment import VirEnvScreen
import requests
import threading
import json
import aiohttp
import asyncio
from threading import Thread

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spatial Audio LiveKit Example App')
room_entry_screen = RoomEntryScreen(screen)
avatar_selection_screen = None
vir_env_screen = None
current_screen = room_entry_screen
running = True

# Join room
async def join_room_async(room_name):
    async with aiohttp.ClientSession() as session:
        url = 'http://127.0.0.1:5000/join_room'  # Adjust as needed
        data = {'room_name': room_name}
        async with session.post(url, json=data) as resp:
            response = await resp.json()
            return {"status_code": resp.status, "message": response}

# Example callback function
def on_join_room_response(result):
    global current_screen
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

async def avatar_selection_async(room_name, username, avatar_image_path, session_id):
    async with aiohttp.ClientSession() as session:
        url = url = 'http://127.0.0.1:5000/avatar_selection'  # Update with your actual server URL
        data = {
            'room_name': room_name,
            'username': username,
            'avatar_image_path': avatar_image_path,
            'session_id': session_id
        }
        async with session.post(url, json=data) as resp:
            response = await resp.json()
            return {"status_code": resp.status, "message": response}

def run_asyncio_coroutine(coroutine, callback):
    """
    Runs an asyncio coroutine in a separate thread and calls the callback
    with the result when done.
    """
    def thread_target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(coroutine)
        loop.close()

        # Call the callback with the result in the main thread
        callback(result)

    thread = threading.Thread(target=thread_target)
    thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen.handle_event(event)
    
    # Update and draw the current screen
    current_screen.update()
    current_screen.draw()

    # Transition logic
    if isinstance(current_screen, RoomEntryScreen) and current_screen.is_done():
        room_name = current_screen.get_room_name()  # Get the entered room name
        coroutine = join_room_async(room_name)
        # The callback function now needs to properly transition to the next screen
        def on_join_room_response(result):
            print("Join room response:", result)
            if result['status_code'] == 200:  # Assuming 200 means success
                room_name = result['message']['room_name']
                session_id = result['message']['session_id']
                
                # Prepare the next screen with the obtained details
                next_screen = AvatarSelectionScreen(screen, room_name, session_id)
                # next_screen.set_room_details(room_name, session_id)
                
                # Transition to the next screen
                global current_screen
                current_screen = next_screen
                # Depending on your game's architecture, you might need to do more here
                # For example, rendering the new screen or triggering its first update/draw cycle.
            else:
                print("Failed to join room:", result['message'])
                # Handle failure - possibly stay on the RoomEntryScreen or show an error message

        run_asyncio_coroutine(coroutine, on_join_room_response)
    elif isinstance(current_screen, AvatarSelectionScreen) and current_screen.is_done():
        avatar_image_path = current_screen.get_selected_image()  # Get the selected avatar image path
        username = current_screen.get_user_name()  # Get the user's chosen username
        session_id = current_screen.get_session_id()  # Get the session ID from the current screen
        
        # Define the callback function for handling the server response
        def on_avatar_selection_response(result):
            if result['status_code'] == 200:  # Assuming 200 means success
                # Server has confirmed the avatar selection
                # Transition to the next screen
                global current_screen
                current_screen = VirEnvScreen(screen, room_name, avatar_image_path, username)  # Assuming you have a NextGameScreen class for the next stage
                # You may want to pass relevant information to the next screen as needed
            else:
                print("Failed to select avatar:", result['message'])
                # Handle failure - possibly show an error message on the current screen
        
        # Package the avatar selection coroutine with the necessary information
        coroutine = avatar_selection_async(
            room_name=current_screen.get_room_name(),
            username=username,
            avatar_image_path=avatar_image_path,
            session_id=session_id
        )
        
        # Run the coroutine in a separate thread and handle the response via the callback
        run_asyncio_coroutine(coroutine, on_avatar_selection_response)    
    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

# if audio_thread is not None:
#     audio_thread.join()
# pygame.quit()
# sys.exit()
