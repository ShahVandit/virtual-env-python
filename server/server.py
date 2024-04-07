from aiohttp import web
import rooms

routes = web.RouteTableDef()

@routes.post('/join')
async def join_room(request):
    data = await request.json()
    room_id = data['room_id']
    user_id = data['user_id']
    offer = data['offer']
    answer = await rooms.join_room(room_id, user_id, offer)
    return web.json_response(answer)

@routes.post('/leave')
async def leave_room(request):
    data = await request.json()
    room_id = data['room_id']
    user_id = data['user_id']
    rooms.leave_room(room_id, user_id)
    return web.json_response({"message": "User left the room."})

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)
