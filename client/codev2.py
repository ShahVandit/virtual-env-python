import pygame
import sys
from screens.room_entry import RoomEntryScreen
from screens.avatar_selection import AvatarSelectionScreen
from screens.virtual_environment import VirEnvScreen

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
        # Transition to the AvatarSelectionScreen
        current_screen = AvatarSelectionScreen(screen, room_name)
    elif isinstance(current_screen, AvatarSelectionScreen) and current_screen.is_done():
        avatar_image = current_screen.get_selected_avatar_image()  # Method to get the selected avatar image
        username = current_screen.get_username()
        # Assuming you have loaded the background and speaker images
        background_image = pygame.image.load('assets\\images\\background\\map.png').convert()
        speaker_image = pygame.image.load('assets\\images\\speaker\\boombox.png').convert_alpha()

        # When transitioning to the VirEnvScreen
        current_screen = VirEnvScreen(screen, room_name, avatar_image, username, background_image, speaker_image)
        current_screen.handle_event(event)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

# if audio_thread is not None:
#     audio_thread.join()
# pygame.quit()
# sys.exit()
