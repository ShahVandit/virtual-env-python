from flask import Flask, request, jsonify
import uuid
from flask_socketio import SocketIO, join_room, emit
import uuid

app = Flask(__name__)
socketio = SocketIO(app)

# A simple in-memory structure to hold rooms and their participants
rooms = {}
users_sessions={}
@app.route('/join_room', methods=['POST'])
def join_room():
    data = request.get_json()
    room_name = data.get('room_name')
    if room_name not in rooms:
        rooms[room_name] = []
    session_id = str(uuid.uuid4())
    rooms[room_name].append({"session_id": session_id, "username": None, "avatar_image_path": None})
    print(rooms[room_name])
    return jsonify({"success": True, "room_name": room_name, "session_id": session_id})


@app.route('/avatar_selection', methods=['POST'])
def avatar_selection():
    data = request.get_json()
    room_name = data.get('room_name')
    username = data.get('username')
    avatar_image_path = data.get('avatar_image_path')
    session_id = data.get('session_id')
    
    # Check if the room exists
    if room_name in rooms:
        # Find the session in the room and update username and avatar_image_path
        for session in rooms[room_name]:
            if session["session_id"] == session_id:
                session["username"] = username
                session["avatar_image_path"] = avatar_image_path
                break
        print(rooms[room_name], room_name)
        return jsonify({"success": True, "room_name": room_name, "session_id": session_id, "username": username})
    else:
        return jsonify({"success": False, "message": "Room does not exist."}), 404


if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
