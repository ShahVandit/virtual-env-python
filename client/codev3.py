import asyncio
import pygame
import socketio
import threading
from screens.room_entry import RoomEntryScreen
from screens.avatar_selection import AvatarSelectionScreen
from screens.virtual_environment import VirEnvScreen
from threading import Thread
import aiohttp

# Initialize Pygame and Socket.IO client
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spatial Audio LiveKit Example App')
room_entry_screen = RoomEntryScreen(screen)
avatar_selection_screen = None
vir_env_screen = None
current_screen = room_entry_screen
sio = socketio.AsyncClient()

# Globals for communication between threads
room_joined = False

async def join_room_async(room_name):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:5000/join_room'  # Adjust as needed
        data = {'room_name': room_name}
        async with session.post(url, json=data) as resp:
            response = await resp.json()
            return {"status_code": resp.status, "message": response}

def on_join_room_response(result):
    print("Join room response:", result)
    if result['status_code'] == 200:  # Assuming 200 means success
        room_name = result['message']['room_name']
        session_id = result['message']['session_id']
        global current_screen
        # Assuming current_screen is accessible and has the set_room_details method
        current_screen = AvatarSelectionScreen(screen, room_name, session_id)
        # Proceed with showing or updating the current screen as necessary
    else:
        # Handle error or unsuccessful attempt to join room
        print("Failed to join room:", result['message'])

async def avatar_selection_async(room_name, username, avatar_image_path, session_id):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:5000/avatar_selection'  # Update with your actual server URL
        data = {
            'room_name': room_name,
            'username': username,
            'avatar_image_path': avatar_image_path,
            'session_id': session_id
        }
        async with session.post(url, json=data) as resp:
            response = await resp.json()
            return {"status_code": resp.status, "message": response}

def on_avatar_selection_response(result):
        global current_screen
        if result['status_code'] == 200:  # Assuming 200 means success
            # Server has confirmed the avatar selection
            # Transition to the next screen
            avatar_image_path = current_screen.get_selected_image()  # Get the selected avatar image path
            username = current_screen.get_user_name()  # Get the user's chosen username
            # session_id = current_screen.get_session_id()
            room_name = result['message']['room_name']
            current_screen = VirEnvScreen(screen, room_name, avatar_image_path, username)  # Assuming you have a NextGameScreen class for the next stage
            # You may want to pass relevant information to the next screen as needed
        else:
            print("Failed to select avatar:", result['message'])

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
# Main Pygame loop
def main():
    global room_joined, join_room_requested, current_screen
    running = True

    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                current_screen.handle_event(event)
        
        # After handling events, check if the operation to join a room is triggered
        if isinstance(current_screen, RoomEntryScreen) and current_screen.done:
            if isinstance(current_screen, RoomEntryScreen) and current_screen.is_done():
                room_name = current_screen.get_room_name()  # Get the entered room name
                coroutine = join_room_async(room_name)
                run_asyncio_coroutine(coroutine, on_join_room_response)
                current_screen.done = False
        elif isinstance(current_screen, AvatarSelectionScreen) and current_screen.is_done():
            avatar_image_path = current_screen.get_selected_image()  # Get the selected avatar image path
            username = current_screen.get_user_name()  # Get the user's chosen username
            session_id = current_screen.get_session_id() 
            coroutine = avatar_selection_async(
            room_name=current_screen.get_room_name(),
            username=username,
            avatar_image_path=avatar_image_path,
            session_id=session_id
            )
            run_asyncio_coroutine(coroutine, on_avatar_selection_response)
            current_screen.done = False

        # if room_joined:
        #     room_name = current_screen.room_name_to_join
        #     current_screen = AvatarSelectionScreen(screen, room_name, "session_id_placeholder")
        #     room_joined = False
        current_screen.update()
        current_screen.draw()
        pygame.display.flip()

def start_asyncio_loop():
    asyncio.new_event_loop().run_forever()

if __name__ == '__main__':
    main()
    # coroutine = join_room_async("example_room")
    # run_asyncio_coroutine(coroutine, on_join_room_response)
# Optional: Clea
