# Placeholder for managing rooms and participants
rooms = {}

async def join_room(room_id, user_id, offer):
    if room_id not in rooms:
        rooms[room_id] = {}
    rooms[room_id][user_id] = offer
    # Simplified: Return a fake answer for demonstration
    return {"answer": "fake_answer"}

def leave_room(room_id, user_id):
    if room_id in rooms and user_id in rooms[room_id]:
        del rooms[room_id][user_id]
        if not rooms[room_id]:  # Room is empty
            del rooms[room_id]
