import threading
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from receiver.models import Request
from sender.auth import handleAuth
from sender.handlers import myHandler, removeUser, watch_new_messages

class RequestData:
    def __init__(self, d):
        self.msgType = d['msgType']

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
    
    async def receive(self, text_data):
        # Send a message to the client
        try:
            print("Entered send message in sendMessageConsunmer")
            d = json.loads(text_data)
            packet = RequestData(d)
            if SendMessageConsumer.user is None and packet.msgType =='auth':
                SendMessageConsumer.user = handleAuth(d,self.send)
            elif SendMessageConsumer.user is not None and packet.msgType == 'auth':
                print("User already exists")
                await self.send(text_data=json.dumps({
                    "text":"User already exists"
                }))
            elif SendMessageConsumer.user is not None and packet.msgType == 'sendMsg':
                print(SendMessageConsumer.user.userId)
                myHandler(packet.msgType, d,SendMessageConsumer.user.userId)
                print("myHandler Executed")
            else:
                print("Authenticate first")
                await self.send(text_data=json.dumps({
                    "text":"Authentiate first"
                }))
                        

        except Exception as error:
            print("An exception occurred:", error)  # prints the full exception message
            print("Exception type:", type(error).__name__)  # prints the exception type (e.g., ZeroDivisionError)

            await self.send(text_data=json.dumps({
                'text': 'exception error in send Consumer'
            }))



class ReceiveMessageConsumer(AsyncWebsocketConsumer):
    user = None
    background_process_started = False
    lock = threading.Lock()

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
        print(text_data)
        print(type(text_data))
        if text_data == "ping":
            await self.send(text_data=json.dumps({
                "text":"pong!"
            }))
        else:
            #after authentication sirf messages recieve honge yha jaise jaise db mai changes honge
            try:
                d = json.loads(text_data)
                packet = RequestData(d)
                if ReceiveMessageConsumer.user is None and packet.msgType=='auth':
                    ReceiveMessageConsumer.user = handleAuth(d,self.send)
                    ReceiveMessageConsumer.background_process_started
                    with ReceiveMessageConsumer.lock:
                        if not ReceiveMessageConsumer.background_process_started:
                            threading.Thread(target=watch_new_messages, args=() ,daemon=True).start()
                            ReceiveMessageConsumer.background_process_started = True
                            print("Background process initiated.")
                elif ReceiveMessageConsumer.user is not None and packet.msgType == 'auth':
                    print("User already exists")
                    await self.send(text_data=json.dumps({
                        "text":"User already exists"
                    }))
            except Exception as error:
                print("An exception occurred:", error)  # prints the full exception message
                print("Exception type:", type(error).__name__)  # prints the exception type (e.g., ZeroDivisionError)

                await self.send(text_data=json.dumps({
                    'text': 'exception error in Recieve consumer'
                }))

        # Optional: Process the message or trigger some action

