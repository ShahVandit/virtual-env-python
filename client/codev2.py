import pygame
import sys
import pyaudio
import wave
import threading
import math
import logging
import time
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors and settings
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RANGE_RADIUS = 100

# Background and avatars
avatar_user = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\doux_preview.png')
audio_file = 'C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\virtual-env-python\client\\public\\disco.wav'
avatar_speaker = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\boombox.png')
background_image = pygame.image.load('C:\\Users\\Vandit\\Desktop\\college\\3d\\project\\virtual-env-python\\client\\public\\map.png')
avatar_user = pygame.transform.scale(avatar_user, (50, 50))
avatar_speaker = pygame.transform.scale(avatar_speaker, (50, 50))

# Initial positions
user_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
speaker_pos = [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3]

# Audio playback flag and lock
logging.basicConfig(level=logging.DEBUG)

audio_lock = threading.Lock()
audio_thread = None
stop_audio_event = threading.Event()
audio_playing = False

def play_audio():
    global audio_playing
    try:
        wf = wave.open(audio_file, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)
        while data and not stop_audio_event.is_set():
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        logging.error(f"Exception in play_audio: {e}")
    finally:
        with audio_lock:
            audio_playing = False
            logging.debug("Audio playback thread ended.")

last_toggle_time = 0
TOGGLE_DEBOUNCE = 0.5  # Debounce time in seconds

def significant_state_change(current_state, new_state):
    """Check if there's a significant change in state that warrants a toggle."""
    return current_state != new_state

def can_toggle():
    """Check if enough time has passed since the last toggle."""
    global last_toggle_time
    current_time = time.time()
    if current_time - last_toggle_time > TOGGLE_DEBOUNCE:
        last_toggle_time = current_time
        return True
    return False


def toggle_audio(user_pos, speaker_pos):
    global audio_playing, audio_thread, stop_audio_event
    distance = math.sqrt((user_pos[0] - speaker_pos[0]) ** 2 + (user_pos[1] - speaker_pos[1]) ** 2)
    within_range = distance <= RANGE_RADIUS
    should_play = within_range and not audio_playing
    should_stop = not within_range and audio_playing

    try:
        if significant_state_change(audio_playing, within_range) and can_toggle():
            with audio_lock:
                if should_play:
                    # Start audio logic
                    if audio_thread is not None and audio_thread.is_alive():
                        stop_audio_event.set()
                        audio_thread.join()  # Ensure previous thread is stopped
                    stop_audio_event.clear()
                    audio_thread = threading.Thread(target=play_audio)
                    audio_thread.start()
                    audio_playing = True
                    logging.debug("Audio started")
                elif should_stop:
                    # Stop audio logic
                    stop_audio_event.set()
                    if audio_thread is not None:
                        audio_thread.join()
                    audio_playing = False
                    logging.debug("Audio stopped")
    except Exception as e:
        logging.error(f"Error in toggle_audio: {e}")
# Main game loop
running = True
in_range_last_frame = False  # Track whether the avatar was in range in the last frame

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            # Toggle audio based on explicit user action within range
            distance = math.sqrt((user_pos[0] - speaker_pos[0])**2 + (user_pos[1] - speaker_pos[1])**2)
            if distance <= RANGE_RADIUS:
                toggle_audio(user_pos, speaker_pos)

    # Movement keys
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

    # Drawing
    screen.blit(background_image, (0, 0))
    screen.blit(avatar_user, user_pos)
    screen.blit(avatar_speaker, speaker_pos)
    pygame.draw.circle(screen, RED, user_pos, RANGE_RADIUS, 1)
    pygame.draw.circle(screen, RED, speaker_pos, RANGE_RADIUS, 1)

    # Toggle audio off if moving out of range, only if the state changed since the last frame
    if in_range_this_frame != in_range_last_frame:
        toggle_audio(user_pos, speaker_pos)
    in_range_last_frame = in_range_this_frame  # Update the range state for the next frame

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
