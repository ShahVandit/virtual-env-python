# Virtual Audio Environment Platform

## Overview
This project creates a virtual environment where users can interact through avatars, communicate via spatial audio, and control music playback within virtual rooms using WebRTC and Socket.IO. It features 3D audio effects using [MIT KEMAR HRTF](https://sound.media.mit.edu/resources/KEMAR.html) to simulate real-world audio.

## Features
- **Spatial Audio**: Utilizes HRTF to provide 3D audio effects, making the audio source appear to come from a specific point in space.
- **Avatar Positioning**: Real-time rendering of avatar positions within the virtual environment.
- **Interactive Music Playback**: Users can control music within their rooms, with sound attenuating based on distance and direction.
- **Real-Time Communication**: Built with Socket.IO for efficient real-time bi-directional communication.

## Prerequisites
Before you start, ensure you have installed:
- Python 3.x


## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**  
   Start by cloning the repository and navigating to the project directory:
   `git clone https://github.com/ShahVandit/virtual-env-python.git`
   `cd virtual-env-python`

2. **Install Dependencies**  
   Install the necessary Python dependencies using:
   `pip install -r requirements.txt`

3. **Start the Server**  
   Change to the server directory and start the server: 
   `cd server`
   `python server3.py`

4. **Launch the Client Application**  
   In a separate terminal window, navigate to the client directory and start the client application:
   `cd ../client`
   `python codev3.py`
