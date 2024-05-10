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
    data = request.get_json()
    room_name = data.get('room_name')
    if room_name not in rooms:
        rooms[room_name] = {"sessions": []}

    # print('join room', rooms[room_name])
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
        rooms[room_name]['is_playing']=False
        rooms[room_name]['played_by']=None
    rooms[room_name]["sessions"].append({"session_id": session_id, "username": username, "avatar_image_path": None})
    try:
        emit('room_update', {'room_name': room_name, 'session_id': session_id, 'username': username, 'total_users':len(rooms[room_name]['sessions'])}, to=request.sid)
    except:
        print('not emmited')

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
        emit('avatar_update', {'session_id': session_id, 'avatar_image_path': avatar_image_path, 'user_name':user_name,'room_name':room_name, 'total_users':len(rooms[room_name]['sessions'])})

@socketio.on('player_position')
def on_update_position(data):
    session_id = data['session_id']
    username = data['username']
    room = data['room_name']
    position = data['position']

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

@socketio.on('request_start_audio')
def handle_request_start_audio(data):
    print('request start called')
    print('-----------')
    room_name = data['room_name']
    # Logic to determine if audio should start playing, e.g.:
    try:
        # if not rooms[room_name]['is_playing']:
        rooms[room_name]['is_playing'] = True
        rooms[room_name]['played_by']=data['user_name']
        print('from ',rooms[room_name]['is_playing'], rooms[room_name]['played_by'])
        # Start streaming audio logic...
        emit('audio_status', {'is_playing': True,'played_by':data['user_name']}, room=room_name)
    except Exception as e:
        print('fds ',e)

@socketio.on('send_audio_status')
def send_audio_status(data):
    room_name=data['room_name']
    print('sending audio status', rooms[room_name])
    print('send_audio_status', rooms[room_name]['is_playing'], rooms[room_name]['played_by'])
    emit('receive_audio_status',{'is_playing':rooms[room_name]['is_playing'], 'played_by':rooms[room_name]['played_by']})

@socketio.on('request_stop_audio')
def handle_request_stop_audio(data):
    room_name = data['room_name']
    if rooms[room_name]['is_playing']:
        rooms[room_name]['is_playing'] = False
        rooms[room_name]['played_by']=None
        print('stop audio requested',rooms[room_name])
        # Stop streaming audio logic...
        emit('audio_status', {'is_playing': False,'played_by':None}, room=room_name)

@socketio.on('audio_chunk')
def send_audio_chunk(data):

    try:
        emit('get_audio_chunk', {'chunk':data['chunk'], 'room_name':data['room_name']}, room=data['room_name'])
    except Exception as e:
        print('asdas ',e)

@socketio.on('get_players')
def handle_get_players(data):
    room_name = data['room_name']
    sessions = rooms.get(room_name, {}).get('sessions', [])
    players_info = [{'username': session['username'], 
                     'position': session.get('position', [0, 0]), 
                     'avatar_image_path': session['avatar_image_path']} 
                    for session in sessions if 'username' in session]
    
    emit('handle_get_players', {'players': players_info}, to=request.sid)
if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
