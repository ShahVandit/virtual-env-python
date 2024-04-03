import pygame
import math
import wave
import pyaudio
import queue
import threading
import pickle
import numpy as np
from scipy.signal import fftconvolve

pygame.init()

with open('hrtf_data.pkl', 'rb') as file:
    # Load the hrtf data from the file
    hrtf_data_loaded = pickle.load(file)

# Window dimensions
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
circle_radius = 50

speaker_pos = [200,200]
speaker_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\boombox.png') 
# pygame.mixer.music.load("C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\disco.mp3")
# pygame.mixer.music.play(-1)  # -1 for infinite loop
# pygame.mixer.music.set_volume(0)  # Start with music muted

def apply_hrtf(data, angle):

    # This is where you would use the actual HRTF data to process the audio chunk
    # The following is a simplified placeholder using fftconvolve for demonstration
    processed_left = fftconvolve(data, hrtf_left, mode='same')
    processed_right = fftconvolve(data, hrtf_right, mode='same')
    return np.vstack((processed_left, processed_right)).T # Return as stereo

def calculate_volume_based_on_distance(player_pos, source_pos, max_distance):
    """
    Calculate the volume based on the distance between Player 1 and the source,
    with the volume dropping off to 0 at max_distance.
    """
    distance = math.sqrt((player_pos[0] - source_pos[0])**2 + (player_pos[1] - source_pos[1])**2)
    if distance >= max_distance:
        return 0
    else:
        # Simple linear attenuation model
        return 1 - (distance / max_distance)

def calculate_distance_and_angle(pos1, pos2):
    distance = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
    angle_radians = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
    angle_degrees = math.degrees(angle_radians)
    return distance, angle_degrees

def is_within_speaker_range(player_pos, speaker_pos, range_radius):
    return math.sqrt((player_pos[0] - speaker_pos[0])**2 + (player_pos[1] - speaker_pos[1])**2) <= speaker_range_radius


# Set the title of the window
pygame.display.set_caption('Virtual Playground')
player1_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\project\\virtual-env-python\\client\\public\\doux_preview.png')
player2_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\mort_preview.png')
pygame.mixer.init() 
pygame.font.init()  # Initialize the font module
font = pygame.font.Font(None, 36)

# Initialize player positions
player1_pos = [100, 100]  # Example starting position for player 1
player2_pos = [200, 100]  # Example starting position for player 2
# left_volume, right_volume = calculate_pan_and_volume(player1_pos, player2_pos, 100)
# channel = sound.play(-1)  # Loop indefinitely
# channel.set_volume(left_volume, right_volume)

# Load and scale the background image
background_image = pygame.image.load('public/map.png')  # Ensure this path is correct
background_image = pygame.transform.scale(background_image, (window_width, window_height))
speaker_range_radius = 150 

music_playing = False
last_toggler = None  # 'player1' or 'player2'
# Main game loop
running = True
audio_queue = queue.Queue()
audio_thread = threading.Thread(target=audio_processing_thread, args=(audio_queue,))
# audio_thread.start()
# audio_thread = threading.Thread(target=stream_audio, args=(param_queue,))
# audio_thread.start()
while running:
    toggled_this_frame = False  # Add a flag to prevent multiple toggles in one frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Get pressed keys
    keys = pygame.key.get_pressed()
    
    # Player 1 movement with arrow keys
    if keys[pygame.K_LEFT]:
        player1_pos[0] -= 1
    if keys[pygame.K_RIGHT]:
        player1_pos[0] += 1
    if keys[pygame.K_UP]:
        player1_pos[1] -= 1
    if keys[pygame.K_DOWN]:
        player1_pos[1] += 1

    # Player 2 movement with WASD keys
    if keys[pygame.K_a]:
        player2_pos[0] -= 1
    if keys[pygame.K_d]:
        player2_pos[0] += 1
    if keys[pygame.K_w]:
        player2_pos[1] -= 1
    if keys[pygame.K_s]:
        player2_pos[1] += 1

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw players
    screen.blit(player1_image, player1_pos)
    screen.blit(player2_image, player2_pos)
    # Draw speaker
    screen.blit(speaker_image, speaker_pos)
    pygame.draw.circle(screen, (100, 100, 100), speaker_pos, speaker_range_radius, 1)  # Draw range circle
    player1_in_range = is_within_speaker_range(player1_pos, speaker_pos, speaker_range_radius)
    player2_in_range = is_within_speaker_range(player2_pos, speaker_pos, speaker_range_radius)
    if player1_in_range and music_playing:
        volume = calculate_volume_based_on_distance(player1_pos, speaker_pos, 150)
        pygame.mixer.music.set_volume(volume)
    elif not player1_in_range:
        pygame.mixer.music.set_volume(0)  # Mute if out of range
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t and not toggled_this_frame:
                if player1_in_range or player2_in_range:
                    # Determine if the player trying to toggle is within range
                    toggler_in_range = 'player1' if player1_in_range else ('player2' if player2_in_range else None)

                    # Allow toggling off by either player if the music is playing
                    if music_playing:
                        music_playing = False
                        last_toggler = None  # Clear the last toggler since the music is stopped
                        pygame.mixer.music.stop()  # Stop the music
                    # Allow toggling on only if the action comes from a player within range who is also the last toggler or if no one has toggled yet
                    elif toggler_in_range and (last_toggler is None or last_toggler == toggler_in_range):
                        music_playing = True
                        print('playing')
                        last_toggler = toggler_in_range  # Update the last toggler
                        distance,angle = calculate_distance_and_angle(player1_pos, speaker_pos)  # Your method to determine the sound direction
                        rounded_angle = 5 * round(angle / 5)
                        rounded_angle = min(hrtf_data_loaded.keys(), key=lambda x: abs(x - rounded_angle))

                        # Reload and play the music from the start
                        # pygame.mixer.music.load("C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\disco.mp3")
                        # pygame.mixer.music.play(-1)  # -1 for infinite loop

                    toggled_this_frame = True  # Prevent further toggles in this frame

    if music_playing and last_toggler is not None:
        player_name_text = font.render(last_toggler + " is playing the music", True, (255, 255, 255))
        screen.blit(player_name_text, (10, 10))  # Position the text at the top-left corner
    pygame.draw.circle(screen, (255, 0, 0), player1_pos, circle_radius, 2)  # Red circle for player 1
    pygame.draw.circle(screen, (0, 0, 255), player2_pos, circle_radius, 2)  # Blue circle for player 2
    # if player1_in_range:
    #     hrtf_left, hrtf_right = select_hrtf_for_azimuth(angle)

    distance, angle = calculate_distance_and_angle(player1_pos, speaker_pos)
    print(f"Distance: {distance:.2f}, Angle: {angle+90:.2f} degrees") 

    pygame.display.flip()


audio_queue.put((None, None))
# audio_thread.join()
pygame.quit()
