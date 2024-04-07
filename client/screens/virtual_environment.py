# vir_env.py
import pygame
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
SCREEN_WIDTH,SCREEN_HEIGHT=800, 600
should_play_audio = False
audio_playing = False
with open('hrtf_data.pkl', 'rb') as file:
    # Load the hrtf data from the file
    hrtf_data_loaded = pickle.load(file)

class VirEnvScreen:
    def __init__(self, screen, room_name, avatar_image, username, background_image, speaker_image):
        self.screen = screen
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.room_name = room_name
        self.avatar_image = avatar_image  # Assuming this is a Surface object
        self.username = username
        self.background_image = background_image  # This should be a Surface object
        self.speaker_image = speaker_image  # This should also be a Surface object
        self.font = pygame.font.Font(None, 36)
        self.user_pos = [self.screen.get_width() // 2, self.screen.get_height() // 2]
        self.speaker_pos = [self.screen.get_width() // 3, self.screen.get_height() // 3]
        self.range_radius = 150
        self.audio_playing = False
        self.audio_thread = None
        # Assume hrtf_data_loaded is available
        # You might need to pass it as a parameter if it's used in methods like play_audio
    def handle_event(self, event):
        # Handling KEYDOWN events to start movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
            elif event.key == pygame.K_UP:
                self.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.moving_down = True
            elif event.key == pygame.K_x:
                if audio_playing:
                    self.stop_audio()
                else:
                    if self.is_user_in_range():
                        self.start_audio()
                # Audio toggle logic remains the same
                
        # Handling KEYUP events to stop movement
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False
            elif event.key == pygame.K_UP:
                self.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.moving_down = False

    def update(self):
        if self.moving_left:
            self.user_pos[0] -= 3
        if self.moving_right:
            self.user_pos[0] += 3
        if self.moving_up:
            self.user_pos[1] -= 3
        if self.moving_down:
            self.user_pos[1] += 3
        # Update anything that needs refreshing
        pass
    def draw(self):
        # Draw the virtual environment
        self.screen.blit(self.background_image, (0, 0))  # Draw background

        # Draw the room name at the top
        room_name_surf = self.font.render(f"Room: {self.room_name}", True, pygame.Color('black'))
        room_name_rect = room_name_surf.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(room_name_surf, room_name_rect)

        # Draw the speaker
        speaker_rect = self.speaker_image.get_rect(center=(self.speaker_pos[0], self.speaker_pos[1]))
        self.screen.blit(self.speaker_image, speaker_rect)

        # Draw the avatar
        avatar_rect = self.avatar_image.get_rect(center=(self.user_pos[0], self.user_pos[1]))
        self.screen.blit(self.avatar_image, avatar_rect)

        # Draw the username above the avatar
        username_surf = self.font.render(self.username, True, pygame.Color('black'))
        username_rect = username_surf.get_rect(center=(avatar_rect.centerx, avatar_rect.top - 20))
        self.screen.blit(username_surf, username_rect)
    def start_audio(self):
        global audio_playing, audio_thread
        if not audio_playing:
            audio_playing = True
            # Pass current user and speaker positions to the audio playback thread
            audio_thread = threading.Thread(target=self.play_audio,)
            audio_thread.start()
    def stop_audio(self):
        global audio_playing
        audio_playing = False
        # Optionally, wait for the thread to finish if you need a clean stop
        if audio_thread is not None:
            audio_thread.join()
        
    def is_user_in_range(self):
        range_radius=150
        distance = math.sqrt((self.user_pos[0] - self.speaker_pos[0])**2 + (self.user_pos[1] - self.speaker_pos[1])**2)
        return distance <= range_radius
    def calculate_distance_and_angle(self, user_pos, speaker_pos):
        dx = self.speaker_pos[0] - self.user_pos[0]
        dy = self.speaker_pos[1] - self.user_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        # Calculate angle from the avatar's perspective
        actual_angle = math.degrees(math.atan2(dy, dx))
        
        # Normalize the angle to be between 0 and 360 degrees
        actual_angle = actual_angle % 360

        # Find the closest available angle in the HRTF data
        rounded_angle = 5 * round(actual_angle / 5)
        closest_angle = rounded_angle if rounded_angle in hrtf_data_loaded else min(hrtf_data_loaded.keys(), key=lambda k: abs(k - rounded_angle))
        
        return distance, actual_angle, closest_angle
    def apply_hrtf(self,audio_data, hrtf_filter, volume_factor):
        # Apply HRTF filter separately to each channel
        processed_audio_left = fftconvolve(audio_data[:, 0], hrtf_filter[:, 0], mode='same')
        processed_audio_right = fftconvolve(audio_data[:, 1], hrtf_filter[:, 1], mode='same')
        
        # Combine the channels back into stereo audio data
        processed_audio = np.stack((processed_audio_left, processed_audio_right), axis=-1)
        
        # Apply volume attenuation
        processed_audio = self.apply_volume_attenuation(processed_audio, volume_factor)
        
        return processed_audio
    def apply_volume_attenuation(self, audio_data, volume_factor):
    # Apply volume attenuation to both channels
        return audio_data * volume_factor
    def play_audio(self):
        global audio_playing, hrtf_data_loaded, user_pos, speaker_pos
        audio_file="assets\\audio\\water.wav"
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

            if self.is_user_in_range():
                distance, _, closest_angle_key = self.calculate_distance_and_angle(self.user_pos, self.speaker_pos)
                hrtf_filter = hrtf_data_loaded[closest_angle_key]
                
                # Calculate volume attenuation factor based on distance
                # Example simple linear attenuation, adjust according to your needs
                volume_factor = max(1 - (distance / 200), 0)  # Adjust the denominator as needed
                
                processed_chunk = self.apply_hrtf(audio_chunk, hrtf_filter, volume_factor)
                stream.write(processed_chunk.astype(np.int16).tobytes())
            else:
                # Write silence if out of range
                silence = np.zeros((chunk_size, 2), dtype=np.int16)
                stream.write(silence.tobytes())

        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()

    def is_done(self):
        # In a real application, you might use this to transition to another state
        return False
