import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
import websockets
import json

async def connect_to_signaling_server(uri):
    async with websockets.connect(uri) as websocket:
        # Example: Sending an offer to the signaling server
        offer = {"sdp": "offer_sdp_here", "type": "offer"}
        await websocket.send(json.dumps(offer))

        # Wait for an answer from the signaling server
        answer = await websocket.recv()
        print("Received answer:", answer)

async def main():
    await connect_to_signaling_server('ws://localhost:8080/ws')

asyncio.run(main())
