from scipy.signal import fftconvolve

def spatialize_audio(angle, distance, sound_file, hrtf_data):
    # Calculate azimuth and distance
    azimuth, distance = calculate_azimuth_distance(player_pos, sound_pos)
    
    # Select appropriate HRTF based on azimuth
    hrtf_left, hrtf_right = select_hrtf_for_azimuth(hrtf_data, azimuth)
    
    # Load the audio file
    sound, fs = load_sound(sound_file)
    
    # Process audio with HRTF
    left_channel = convolve(sound, hrtf_left)
    right_channel = convolve(sound, hrtf_right)
    
    # Adjust volume based on distance
    volume_adjusted_audio = adjust_volume_for_distance(left_channel, right_channel, distance)
    
    # Play back the processed audio
    play_audio(volume_adjusted_audio, fs)


def convolve(signal, hrtf):
    """
    Convolve an audio signal with an HRTF filter.

    Parameters:
    - signal: The audio signal (numpy array).
    - hrtf: The HRTF filter (numpy array).

    Returns:
    - The convolved audio signal.
    """
    # Ensure the signal and HRTF are 1D numpy arrays for convolution
    signal = signal.flatten()
    hrtf = hrtf.flatten()

    # Apply convolution
    convolved_signal = fftconvolve(signal, hrtf, mode='same')
    return convolved_signal