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
pygame.display.set_caption('Welcome to Virtual Environment')
room_entry_screen = RoomEntryScreen(screen)
avatar_selection_screen = None
vir_env_screen = None
current_screen = room_entry_screen
sio = socketio.AsyncClient()

# @sio.event
# async def room_update():
#     print("Connected to the server.")
# Globals for communication between threads
# room_joined = False

async def join_room_async(room_name):
    await sio.connect('http://localhost:5000')
    # Emit the 'join' event to the server with the room name and username
    await sio.emit('join', {'room_name': room_name, 'username':None})

async def update_screen(data):
    print("Room update received:", data)
    # Assuming data contains 'room_name', 'session_id', and 'username'
    room_name = data['room_name']
    session_id = data['session_id']
    username = data['username']
    total_users=data['total_users']
    
    # Update your application state or UI here
    global current_screen
    # Assuming you have an appropriate way to switch to the AvatarSelectionScreen
    # and that it can be initialized with these parameters
    current_screen = AvatarSelectionScreen(screen, room_name, session_id, total_users)

@sio.event
async def room_update(data):
    await update_screen(data)
    
@sio.event
async def send_position(data):
    """Receive position updates from the server and update the game environment."""
    username = data['username']
    position = data['position']
    avatar_image_path = data['avatar_image_path']
    print(f"postion {position} received from {username}")
    current_screen.update_other_user_positions(username, position, avatar_image_path)

async def avatar_selection_async(room_name, username, avatar_image_path, session_id):
    try:
        # await sio.connect('http://localhost:5000')
        data = {
            'room_name': room_name,
            'username': username,
            'avatar_image_path': avatar_image_path,
            'session_id': session_id
        }
        print("Sending select_avatar event with data:", data)  # Add logging
        await sio.emit('select_avatar', data)
        print("select_avatar event emitted successfully")  # Add logging
    except Exception as e:
        print("Error:", e)  # Add error handling/logging

def on_avatar_selection_response(result):
    room_name = result['room_name']
    session_id = result['session_id']
    username = result['user_name']
    total_users=result['total_users']
    avatar_image_path=result['avatar_image_path']
    global current_screen
    current_screen = VirEnvScreen(screen, room_name, avatar_image_path, username,session_id)

@sio.event
def avatar_update(data):
    on_avatar_selection_response(data)

def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
# Main Pygame loop
def main():
    global room_joined, join_room_requested, current_screen
    running = True

    # Initialize Pygame and set up your screens, etc.
    pygame.init()
    current_screen = RoomEntryScreen(screen)

    # Start the asyncio event loop for Socket.IO in a separate thread

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_asyncio_loop, args=(loop,), daemon=True)
    t.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                current_screen.handle_event(event)
        
        # Check if it's time to join a room based on your application's logic
        if isinstance(current_screen, RoomEntryScreen) and current_screen.is_done():
            room_name = current_screen.get_room_name()  # Get the entered room name
            asyncio.run_coroutine_threadsafe(main_coroutine(room_name), loop)            
            current_screen.done = False
        elif isinstance(current_screen, AvatarSelectionScreen) and current_screen.is_done():
            print('here')
            avatar_image_path = current_screen.get_selected_image()  # Get the selected avatar image path
            username = current_screen.get_user_name()  # Get the user's chosen username
            session_id = current_screen.get_session_id() 
            room_name=current_screen.get_room_name()
            asyncio.run_coroutine_threadsafe(avatar_selection_async(room_name, username, avatar_image_path, session_id), loop)
            current_screen.done = False
        elif isinstance(current_screen, VirEnvScreen):
            if current_screen.has_moved():
                position = current_screen.get_user_pos()
                asyncio.run_coroutine_threadsafe(
                    sio.emit('player_position', {'username': current_screen.username, 'position': position, 'room_name':current_screen.room_name, 'session_id':current_screen.session_id}), loop)


        # if room_joined:
        #     room_name = current_screen.room_name_to_join
        #     current_screen = AvatarSelectionScreen(screen, room_name, "session_id_placeholder")
        #     room_joined = False
        current_screen.update()
        current_screen.draw()
        pygame.display.flip()
    loop.call_soon_threadsafe(loop.stop)

async def main_coroutine(room_name):
    await join_room_async(room_name)

if __name__ == '__main__':
    main()
    # coroutine = join_room_async("example_room")
    # run_asyncio_coroutine(coroutine, on_join_room_response)
# Optional: Clea
