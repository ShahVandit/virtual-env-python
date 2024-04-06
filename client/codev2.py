import pygame
import sys
from room_entry import RoomEntryScreen
from avatar_selection import AvatarSelectionScreen
from virtual_env import VirEnvScreen

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spatial Audio LiveKit Example App')

# Initialize RoomEntryScreen
room_entry_screen = RoomEntryScreen(screen)
current_screen = room_entry_screen  # Start with the room entry screen

# Main game loop
running = True
room_name = ''  # Variable to store the room name
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen.handle_event(event)

    current_screen.update()
    screen.fill(pygame.Color('white'))  # Clear screen
    current_screen.draw()
    pygame.display.flip()  # Update the display

    # Transition logic
    if isinstance(current_screen, RoomEntryScreen) and current_screen.is_done():
        room_name = current_screen.get_room_name()  # Get the entered room name
        # Now transition to the AvatarSelectionScreen
        current_screen = AvatarSelectionScreen(screen, room_name)
    elif isinstance(current_screen, AvatarSelectionScreen) and current_screen.is_done():
        room_name = current_screen.room_name
        avatar_image = current_screen.avatars[current_screen.selected_avatar_index][0]  # Get the avatar Surface
        username = current_screen.username
        # Transition to the virtual environment screen
        current_screen = VirEnvScreen(screen, room_name, avatar_image, username)

pygame.quit()
sys.exit()
