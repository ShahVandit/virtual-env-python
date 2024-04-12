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
def join_room_():
    # This endpoint might not be necessary for SocketIO,
    # but kept for initial room creation or other setup steps.
    data = request.get_json()
    room_name = data.get('room_name')
    if room_name not in rooms:
        rooms[room_name] = {"sessions": []}
    return jsonify({"success": True, "room_name": room_name})

@socketio.on('join')
def on_join(data):
    username = data['username']
    room_name = data['room_name']
    session_id = str(uuid.uuid4())
    print('join received')
    join_room(room_name)
    # print(rooms)
    if room_name not in rooms:
        rooms[room_name] = {"sessions": []}
    rooms[room_name]["sessions"].append({"session_id": session_id, "username": username, "avatar_image_path": None})
    try:
        emit('room_update', {'room_name': room_name, 'session_id': session_id, 'username': username, 'total_users':len(rooms[room_name]['sessions'])}, to=request.sid)
    except:
        print('not emmited')
    print(rooms)

@socketio.on('select_avatar')
def on_select_avatar(data):
    room_name = data['room_name']
    session_id = data['session_id']
    user_name=data['username']
    avatar_image_path = data['avatar_image_path']
    # Update the session with the new avatar
    if room_name in rooms:
        for session in rooms[room_name]["sessions"]:
            if session["session_id"] == session_id:
                session["avatar_image_path"] = avatar_image_path
                session['username']=user_name
                break

        print('emitt',{'session_id': session_id, 'avatar_image_path': avatar_image_path, 'user_name':user_name,'room_name':room_name})
        emit('avatar_update', {'session_id': session_id, 'avatar_image_path': avatar_image_path, 'user_name':user_name,'room_name':room_name, 'total_users':len(rooms[room_name]['sessions'])})

@socketio.on('player_position')
def on_update_position(data):
    session_id = data['session_id']  # Assuming session_id corresponds to the client's Socket.IO session id
    username = data['username']
    room = data['room_name']
    position = data['position']

    print(username,'update data from')
    # Find the correct session and update the position
    found = False
    if room in rooms:
        for session in rooms[room]['sessions']:
            if session['session_id'] == session_id:
                # Assume you add a 'position' field to the session dict
                session['position'] = position
                found = True
                break
    if not found:
        print(f"Session {session_id} not found in room {room}")
        return
    # Broadcast the new position to all clients in the room except the sender
    emit('send_position', {
        'username': username, 
        'position': position, 
        'avatar_image_path': session.get('avatar_image_path')
    }, room=room, include_self=False)
if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
