import pygame
import sys
import pyaudio
import wave
import threading
import math
import logging
import time
import numpy as np
import pickle
from scipy.signal import fftconvolve
import soundfile as sf
from screens.room_entry import RoomEntryScreen

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# State management
current_screen = RoomEntryScreen(screen)
chunk = 1024

audio_path='C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\virtual-env-python\\client\\public\\water.wav'
p = pyaudio.PyAudio()

with open('hrtf_data.pkl', 'rb') as file:
    # Load the hrtf data from the file
    hrtf_data_loaded = pickle.load(file)
print(hrtf_data_loaded.keys())
# Colors and settings
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RANGE_RADIUS = 100

# Background and avatars
avatar_user = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\virtual-env-python\\client\\assets\\images\\avatars\\doux_preview.png')
audio_file = 'C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\virtual-env-python\\client\\assets\\audio\\water.wav'
avatar_speaker = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\virtual-env-python\\client\\assets\\images\\speaker\\boombox.png')
background_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\virtual-env-python\\client\\assets\\images\\background\\map.png')
avatar_user = pygame.transform.scale(avatar_user, (50, 50))
avatar_speaker = pygame.transform.scale(avatar_speaker, (50, 50))

# Initial positions
user_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
speaker_pos = [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3]

# Function to play audio
should_play_audio = False
audio_playing = False

def calculate_distance_and_angle(user_pos, speaker_pos):
    dx = speaker_pos[0] - user_pos[0]
    dy = speaker_pos[1] - user_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    # Calculate angle from the avatar's perspective
    actual_angle = math.degrees(math.atan2(dy, dx))
    
    # Normalize the angle to be between 0 and 360 degrees
    actual_angle = actual_angle % 360

    # Find the closest available angle in the HRTF data
    rounded_angle = 5 * round(actual_angle / 5)
    closest_angle = rounded_angle if rounded_angle in hrtf_data_loaded else min(hrtf_data_loaded.keys(), key=lambda k: abs(k - rounded_angle))
    
    return distance, actual_angle, closest_angle

# Audio playback function

# def apply_volume_attenuation(data, volume):
#     """Apply volume attenuation to audio frames."""
#     # Convert byte data to numpy array
#     audio_samples = np.frombuffer(data, dtype=np.int16)
#     # Apply volume factor
#     attenuated_samples = (audio_samples * volume).astype(np.int16)
#     # Convert back to bytes
#     return attenuated_samples.tobytes()

def apply_volume_attenuation(audio_data, volume_factor):
    # Apply volume attenuation to both channels
    return audio_data * volume_factor

def apply_hrtf(audio_data, hrtf_filter, volume_factor, angle):
    if angle > 180:
    # Apply HRTF filter but switch channels for angles greater than 180
        processed_audio_left = fftconvolve(audio_data[:, 0], hrtf_filter[:, 1], mode='same')
        processed_audio_right = fftconvolve(audio_data[:, 1], hrtf_filter[:, 0], mode='same')
    else:
        # Apply HRTF filter normally for angles 180 or less
        processed_audio_left = fftconvolve(audio_data[:, 0], hrtf_filter[:, 0], mode='same')
        processed_audio_right = fftconvolve(audio_data[:, 1], hrtf_filter[:, 1], mode='same')

# Combine the channels back into stereo audio data
    processed_audio = np.stack((processed_audio_left, processed_audio_right), axis=-1)
    # Apply volume attenuation
    processed_audio = apply_volume_attenuation(processed_audio, volume_factor)
    
    return processed_audio

def play_audio():
    global audio_playing, hrtf_data_loaded, user_pos, speaker_pos

    # Load the audio file
    data, samplerate = sf.read(audio_file)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=samplerate,
                    output=True)


    chunk_size = 1024  # Define your chunk size
    num_chunks = len(data) // chunk_size
    for i in range(num_chunks + 1):
        if not audio_playing:
            break

        chunk_start = i * chunk_size
        chunk_end = chunk_start + chunk_size
        audio_chunk = data[chunk_start:chunk_end]

        if is_user_in_range():
            distance, angle, closest_angle_key = calculate_distance_and_angle(user_pos, speaker_pos)
            hrtf_filter = hrtf_data_loaded[closest_angle_key]
            
            # Calculate volume attenuation factor based on distance
            # Example simple linear attenuation, adjust according to your needs
            volume_factor = max(1 - (distance / 200), 0)  # Adjust the denominator as needed
            
            processed_chunk = apply_hrtf(audio_chunk, hrtf_filter, volume_factor, angle)
            stream.write(processed_chunk.astype(np.int16).tobytes())
        else:
            # Write silence if out of range
            silence = np.zeros((chunk_size, 2), dtype=np.int16)
            stream.write(silence.tobytes())

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

audio_playing = False

# Define a thread for audio playback to be controlled
audio_thread = None

def start_audio():
    global audio_playing, audio_thread
    if not audio_playing:
        audio_playing = True
        # Pass current user and speaker positions to the audio playback thread
        audio_thread = threading.Thread(target=play_audio,)
        audio_thread.start()

def stop_audio():
    global audio_playing
    audio_playing = False
    # Optionally, wait for the thread to finish if you need a clean stop
    if audio_thread is not None:
        audio_thread.join()
range_radius=150
# Function to check if the user is in the range of the speaker
def is_user_in_range():
    distance = math.sqrt((user_pos[0] - speaker_pos[0])**2 + (user_pos[1] - speaker_pos[1])**2)
    return distance <= range_radius

# Main game loop
running = True
audio_playing=False
in_range_last_frame = False  # Track whether the avatar was in range in the last frame
audio_thread = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen.handle_event(event)

    # Update and draw the current screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if audio_playing:
                    stop_audio()
                else:
                    if is_user_in_range():
                        start_audio()

    # Movement keys
    current_screen.update()
    current_screen.draw()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        user_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        user_pos[0] += 5
    if keys[pygame.K_UP]:
        user_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        user_pos[1] += 5

    # Calculate current distance and check range
    distance = math.sqrt((user_pos[0] - speaker_pos[0])**2 + (user_pos[1] - speaker_pos[1])**2)
    in_range_this_frame = distance <= RANGE_RADIUS
    distance, angle, closest_angle = calculate_distance_and_angle(user_pos, speaker_pos)
    print(f"Distance: {distance:.2f}, Angle: {angle:.2f} degrees, Closest HRTF: ", {closest_angle})
    # Drawing
    screen.blit(background_image, (0, 0))
    screen.blit(avatar_user, user_pos)
    screen.blit(avatar_speaker, speaker_pos)
    pygame.draw.circle(screen, RED, user_pos, RANGE_RADIUS, 1)
    pygame.draw.circle(screen, RED, speaker_pos, RANGE_RADIUS, 1)

    # Toggle audio off if moving out of range, only if the state changed since the last frame
    # if in_range_this_frame != in_range_last_frame:
    #     toggle_audio(user_pos, speaker_pos)
    # in_range_last_frame = in_range_this_frame  # Update the range state for the next frame

    # Update the display
    # toggle_audio(user_pos, speaker_pos)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

audio_thread.join()
pygame.quit()
sys.exit()