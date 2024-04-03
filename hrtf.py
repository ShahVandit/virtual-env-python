import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample
import scipy
import os
import re

# print(np.__version__)
# print(sf.__version__)
# print(scipy.__version__)
# print(np.__version__)

def load(hrtf_path, target_fs):
    hrtf, fs = sf.read(hrtf_path)
    if fs != target_fs:
        num_samples = int(len(hrtf) * float(target_fs) / fs)
        hrtf = resample(hrtf, num_samples)
    return hrtf

def get_name(filename):
    match = re.search(r'H-?10e(\d+)a\.wav', filename)
    if match:
        return int(match.group(1))
    return None

def play(sound_path, hrtf_folder_right, hrtf_folder_left):
    sound, fs = sf.read(sound_path)
    if sound.ndim == 1:
        sound = np.tile(sound, (2, 1)).T

    hrtf_files_right = [file for file in os.listdir(hrtf_folder_right) if file.endswith('.wav')]
    hrtf_files_left = [file for file in os.listdir(hrtf_folder_left) if file.endswith('.wav')]

    # Sort the HRTF filenames based on the azimuth angle
    hrtf_files_sorted_right = sorted(hrtf_files_right, key=lambda x: get_name(x))
    hrtf_files_sorted_left = sorted(hrtf_files_left, key=lambda x: get_name(x))
    # The total number of HRTF files dictates the chunk size for each azimuth step
    total_hrtf_files = len(hrtf_files_sorted_right) + len(hrtf_files_sorted_left)
    chunk_size = len(sound) // total_hrtf_files

    combined_audio = []

    # Process right channel HRTF files (0 to 180 degrees)
    for i, hrtf_file in enumerate(hrtf_files_sorted_right):
        hrtf_path = os.path.join(hrtf_folder_right, hrtf_file)
        hrtf = load(hrtf_path, fs)

        chunk_start = i * chunk_size
        chunk_end = (i + 1) * chunk_size
        current_chunk = sound[chunk_start:chunk_end]

        # Apply HRTF only to the right channel
        convolved_chunk = current_chunk.copy()
        convolved_chunk[:, 1] = fftconvolve(current_chunk[:, 1], hrtf[:, 1], mode='same')

        combined_audio.append(convolved_chunk)

    # Process left channel HRTF files (180 to 0 degrees)
    for i, hrtf_file in enumerate(hrtf_files_sorted_left):
        hrtf_path = os.path.join(hrtf_folder_left, hrtf_file)
        hrtf = load(hrtf_path, fs)

        chunk_start = (len(hrtf_files_sorted_right) + i) * chunk_size
        chunk_end = (len(hrtf_files_sorted_right) + i + 1) * chunk_size if i < len(hrtf_files_sorted_left) - 1 else len(sound)
        current_chunk = sound[chunk_start:chunk_end]

        # Apply HRTF only to the left channel
        convolved_chunk = current_chunk.copy()
        convolved_chunk[:, 0] = fftconvolve(current_chunk[:, 0], hrtf[:, 0], mode='same')

        combined_audio.append(convolved_chunk)

    combined_audio = np.concatenate(combined_audio, axis=0)

    output_path = 'spatialized_audio.wav'
    sf.write(output_path, combined_audio, fs)
    return output_path


# Example usage
output_file = play('water.wav', 'compact/elev10', 'compact/elev-10')
print(f"Audio saved to: {output_file}")
