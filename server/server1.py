from flask import Flask, request, jsonify
from flask_socketio import SocketIO, join_room, emit
import uuid

app = Flask(__name__)
# Secret key for session management. Replace 'your_secret_key' with a real secret key.
socketio = SocketIO(app)

# A simple in-memory structure to hold rooms and their participants
rooms = {}
# Holds avatar selections
users_sessions = {}

@socketio.on('join_room')
def handle_join_room(data):
    room_name = data['room_name']
    if room_name not in rooms:
        rooms[room_name] = []
    print('called')
    session_id = str(uuid.uuid4())  # Generate a unique session ID for the new user
    rooms[room_name].append(session_id)

    join_room(room_name)  # Subscribe the socket to a given room
    # Notify others in the room
    emit('room_update', {'message': f'{session_id} has joined the room {room_name}'}, room=room_name)

    # Acknowledge the user who just joined
    emit('join_ack', {'session_id': session_id, 'room_name': room_name})

@app.route('/avatar_selection', methods=['POST'])
def avatar_selection():
    data = request.get_json()
    room_name = data.get('room_name')
    username = data.get('username')
    avatar_image_path = data.get('avatar_image_path')
    session_id = data.get('session_id')

    # Store or update the user session with the avatar selection
    users_sessions[session_id] = {
        'room_name': room_name,
        'username': username,
        'avatar_image_path': avatar_image_path
    }

    # Optionally, notify others in the room about the avatar selection
    # For real-time updates, you'd use emit here similarly to join_room
    # emit('avatar_selected', {'session_id': session_id, 'avatar_image_path': avatar_image_path}, room=room_name)

    # Respond with the requested data
    return jsonify({
        "success": True,
        "message": "Avatar selected successfully",
        "room_name": room_name,
        "session_id": session_id,
        "user_name": username,
        "selected_avatar": avatar_image_path
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
