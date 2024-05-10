import json
import pickle
import numpy as np

# Load data from pickle file
with open('hrtf_data.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data[0])

# Convert NumPy arrays to lists
for key, value in data.items():
    if isinstance(value, np.ndarray):
        data[key] = value.tolist()

# Convert data to JSON
# json_data = json.dumps(data, default=convert_numpy)

# Write JSON data to a file
with open('data1.json', 'w') as f:
    json.dump(data, f, indent=4)  # indent argument for pretty formatting

