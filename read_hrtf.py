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

import os
from scipy.io import wavfile

# Path to your 'elev-10' folder
folder_path = 'elev-10'

# Dictionary to store the azimuth angle as key and HRTF data as value
hrtf_data = {}


with open('./client/hrtf_data.pkl', 'rb') as file:
    # Load the hrtf data from the file
    hrtf_data_loaded = pickle.load(file)
print(hrtf_data_loaded[35].shape)
# List all files in the folder
# for filename in os.listdir(folder_path):
#     if filename.endswith('.wav'):
#         # Extract the azimuth angle from the filename
#         # Assuming the format is 'H-10eXXXa.wav' where XXX is the angle
#         angle = int(filename.split('e')[1][:3])
        
#         # Read the HRTF data from the WAV file
#         filepath = os.path.join(folder_path, filename)
#         _, data = wavfile.read(filepath)
        
#         # Add the angle and data to the dictionary
#         hrtf_data[angle+180] = data

# hrtf_data_loaded.update(hrtf_data)

# with open('hrtf_data.pkl', 'wb') as handle:
#     pickle.dump(hrtf_data_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)
# # Now hrtf_data dictionary has the azimuth angle as keys and HRTF data as values


# print(hrtf_data_loaded)


