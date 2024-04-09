import soundfile as sf
import numpy as np
import os

# Function to load HRTF files
def load_hrtf(hrtf_path, azimuth):
    hrtf_files = sorted([f for f in os.listdir(hrtf_path) if f.endswith('.wav')])
    # Handle wrap-around for azimuths beyond 180 degrees
    file_index = azimuth // 5 if azimuth <= 180 else (360 - azimuth) // 5
    hrtf_file = hrtf_files[file_index]
    hrtf, _ = sf.read(os.path.join(hrtf_path, hrtf_file))
    return hrtf

# Function to apply HRTF to a mono audio signal
def apply_hrtf(audio, hrtf):
    if len(audio.shape) > 1:
        audio = audio[:, 0]  # Convert to mono if stereo

    processed_audio_left = np.convolve(audio, hrtf[:, 0], mode='same')
    processed_audio_right = np.convolve(audio, hrtf[:, 1], mode='same')
    processed_audio = np.vstack((processed_audio_left, processed_audio_right)).T
    return processed_audio

# Load the audio file
audio_file_path = 'water.wav'
audio_data, fs = sf.read(audio_file_path)

if len(audio_data.shape) > 1:
    audio_data = audio_data[:, 0]  # Convert to mono if stereo

# Number of steps in the azimuth range for a full 360-degree rotation
num_steps = 72  # 360 degrees / 5 degrees per step

# Split the audio data into segments for each azimuth step
audio_segments = np.array_split(audio_data, num_steps)

# Paths for HRTF files
elev10_path = 'elev10'
elev_minus_10_path = 'elev-10'

processed_segments = []

for i, segment in enumerate(audio_segments):
    azimuth = (i * 5) % 360
    # Choose HRTF path based on azimuth
    hrtf_path = elev10_path if azimuth <= 180 else elev_minus_10_path
    hrtf = load_hrtf(hrtf_path, azimuth)
    processed_segment = apply_hrtf(segment, hrtf)
    processed_segments.append(processed_segment)

# Combine processed segments into the final audio
final_audio = np.vstack(processed_segments)

# Save the final processed audio
output_file_path = 'processed_audio.wav'
sf.write(output_file_path, final_audio, fs)