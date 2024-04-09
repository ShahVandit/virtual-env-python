from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# A simple in-memory structure to hold rooms and their participants
rooms = {}

@app.route('/join_room', methods=['POST'])
def join_room():
    data = request.get_json()
    room_name = data.get('room_name')
    if room_name not in rooms:
        rooms[room_name] = []
    session_id = str(uuid.uuid4())
    rooms[room_name].append(session_id)
    print(rooms)
    return jsonify({"success": True, "room_name": room_name, "session_id": session_id})

users_sessions = {}
@app.route('/avatar_selection', methods=['POST'])
def avatar_selection():
    data = request.get_json()
    room_name = data.get('room_name')
    username = data.get('username')
    avatar_image_path = data.get('avatar_image_path')
    session_id = data.get('session_id')

    # Here, you'd typically validate the provided session_id, room_name, etc.
    # For simplicity, we'll assume the received data is valid and proceed

    # Store or update the user session with the avatar selection
    users_sessions[session_id] = {
        'room_name': room_name,
        'username': username,
        'avatar_image_path': avatar_image_path
    }

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
    app.run(debug=True)
