from aiohttp import web
import uuid
import json
rooms = {}  # Dictionary to keep track of rooms and their participants

async def join_room(request):
    try:
        data = await request.json()
        room_name = data.get('room_name')
        
        if not room_name:
            # Room name is missing or empty
            return web.json_response({"error": "Room name is required."}, status=400)
        
        print(f"Received request to join/create room: '{room_name}'")
        
        session_id = str(uuid.uuid4())
        
        if room_name not in rooms:
            print(f"Room '{room_name}' does not exist. Creating new room.")
            rooms[room_name] = {}
        
        rooms[room_name][session_id] = session_id
        print(rooms[room_name])
        print(f"User with session ID '{session_id}' added to room '{room_name}'")
        
        response_data = {
            "message": "Successfully joined or created the room.",
            "room_name": room_name,
            "session_id": session_id,
            "status":200
        }
        print('----------------------')
        print('sessionmn',response_data['session_id'])
        return web.json_response(response_data)  # OK - Successfully joined/created

    except Exception as e:
        # Catch-all for any other error
        print(f"Error processing request: {e}")
        return web.json_response({"error": "Internal server error", "status":400}, status=500)  # Internal Server Error

async def avatar_selection(request):
    print('func_call')
    try:
        # Parse the request data
        data = await request.json()
        room_name = data['room_name']
        user_name = data['user_name']
        session_id = data['session_id']
        avatar_image = data['avatar_image']
        # Validate the input data
        if not all([room_name, user_name, session_id, avatar_image]):
            return web.json_response({"error": "Missing required data"}, status=400)
        
        # Check if the room exists and the session_id is valid
        if room_name not in rooms or session_id not in rooms[room_name]:
            return web.json_response({"error": "Invalid room or session ID"}, status=404)

        # Update the session_id to be associated with the user_name
        rooms[room_name][session_id] = user_name

        # Optionally, handle the avatar_image according to your application's needs

        # Send back the received details as a response
        response_data = {
            "room_name": room_name,
            "user_name": user_name,
            "session_id": session_id,
            "avatar_image": avatar_image
        }
        print('sessiom', response_data)
        return web.json_response(response_data, status=200)

    except json.JSONDecodeError as e:
        print('json exception',e)
        return web.json_response({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        print('eror',e)
        return web.json_response({"error": "Internal server error: " + str(e)}, status=500)


app = web.Application()
app.add_routes([web.post('/avatar_selection', avatar_selection)])
app.add_routes([web.post('/join', join_room)])

if __name__ == '__main__':
    web.run_app(app,host='localhost', port=8080)
