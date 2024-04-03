# import os
# from scipy.io import wavfile
# import re
# def read_hrtf_data(elev10_dir, elev_minus_10_dir):
#     """
#     Reads HRTF WAV files from specified directories and returns a dictionary with azimuth angles as keys
#     and HRTF data as values.

#     Parameters:
#     - elev10_dir: str, path to the directory with HRTF files for the right side (positive elevation).
#     - elev_minus_10_dir: str, path to the directory with HRTF files for the left side (negative elevation).

#     Returns:
#     - hrtf_dict: dict, a dictionary with azimuth angles as keys and HRTF data as values.
#     """
#     hrtf_dict = {}

#     # Process files in the right elevation directory
#     for filename in os.listdir(elev10_dir):
#         if filename.endswith('.wav'):
#             # Parse the azimuth from the filename
#             match = re.search(r'H-?10e(\d+)a\.wav', filename)
#             if match:
#                 azimuth= int(match.group(1))
#             # azimuth = int(filename.split('e')[1][:-1])  # Extracts the azimuth angle
#             # Read the HRTF data
#             _, data = wavfile.read(os.path.join(elev10_dir, filename))
#             hrtf_dict[azimuth] = data

#     # Process files in the left elevation directory
#     for filename in os.listdir(elev_minus_10_dir):
#         if filename.endswith('.wav'):
#             # Parse the azimuth from the filename (negating it since it's left)
#             match = re.search(r'H-?10e(\d+)a\.wav', filename)
#             if match:
#                 azimuth= int(match.group(1))
#             # Read the HRTF data
#             _, data = wavfile.read(os.path.join(elev_minus_10_dir, filename))
#             hrtf_dict[azimuth] = data

#     return hrtf_dict

# mydic=((read_hrtf_data('elev10', 'elev-10')))

import pickle

# # Assume hrtf_data is your dictionary
# hrtf_data = {...}

# # Saving the dictionary to a file
with open('hrtf_data.pkl', 'rb') as file:
    hrtf_data_loaded = pickle.load(file)
# print(hrtf_data_loaded)


