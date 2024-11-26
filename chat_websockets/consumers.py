from channels.generic.websocket import AsyncWebsocketConsumer
import json

from receiver.models import Request
from sender.handlers import removeUser

class SendMessageConsumer(AsyncWebsocketConsumer):
    user = None

    async def connect(self):
        # Accept WebSocket connection
        await self.accept()
        print("WebSocket for sending messages connected.")

    async def disconnect(self, close_code):
        # Handle disconnection
        print("WebSocket for sending messages disconnected.")
        if self.user is not None:
            removeUser(self.user.userId)


    async def sendMsg(self, message):
        # Send a message to the client
        await self.send(text_data=json.dumps({
            'message': message
        }))

class ReceiveMessageConsumer(AsyncWebsocketConsumer):
    user = None
    
    async def connect(self):
        # Accept WebSocket connection
        await self.accept()
        print("WebSocket for receiving messages connected.")

    async def disconnect(self, close_code):
        # Handle disconnection
        print("WebSocket for receiving messages disconnected.")
        if self.user is not None:
            removeUser(self.user.userId)

    async def receive(self, text_data):
        # Receive a message from the client
        message = json.loads(text_data).get('message', '')
        print(f"Received message from client: {message}")
        # Optional: Process the message or trigger some action

