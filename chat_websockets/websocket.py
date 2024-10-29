# websocket.py

import asyncio
from collections import namedtuple
import json
import threading
from websockets.request_models import Request
from websockets.auth import handleAuth
from websockets.handlers import myHandler, removeUser, watch_new_messages
#from websockets.serializers import deserializer

# connections send
#clients = {}
#ids = {}

background_process_started = False
lock = threading.Lock()
class RequestData:
    def __init__(self, d):
        self.msgType = d['msgType']

async def websocket_application(scope, receive, send):
    user = None
    while True:
        try:
            event = await receive()

            request = Request(**event)

            if request.type == 'websocket.connect':
                await send({
                    'type': 'websocket.accept'
                })

            if request.type == 'websocket.disconnect':
                if user is not None:
                    removeUser(user.userId)

            if request.type == 'websocket.receive':
                print(request.text)
                if request.text == 'ping':
                    await send({
                        'type': 'websocket.send',
                        'text': 'pong!'
                    })
                else:
                    #data required by client in text->msg_type,from,to,message
                    try:
                        # request=deserializer(str(event['text']))
                        print("entered else")
                        d = json.loads(str(event['text']))
                        packet = RequestData(d)
                        if packet.msgType =='auth':
                            user = handleAuth(d,send)
                            global background_process_started
                            with lock:
                                if not background_process_started:
                                    threading.Thread(target=watch_new_messages, args=() ,daemon=True).start()
                                    background_process_started = True
                                    print("Background process initiated.")
                        elif user is not None:
                            print(user.userId)
                            myHandler(packet.msgType, d,user.userId)
                            # print("myHandler executed")
                            # if response is not None:
                            #     response.update({'msg_type':request['msg_type']})
                            #     print("response:",response)
                            #     await send({
                            #         'type': 'websocket.send',
                            #         'text': json.dumps(response)
                            #     })
                        else:
                            raise TypeError("Authenticate first")
                    except Exception as error:
                        print("An exception occurred:", error)  # prints the full exception message
                        print("Exception type:", type(error).__name__)  # prints the exception type (e.g., ZeroDivisionError)

                        await send({
                            'type': 'websocket.send',
                            'text': 'exception error'
                        })
        
        except asyncio.CancelledError:
            print("WebSocket connection was canceled.")
            # Perform any cleanup here, if necessary.
        except Exception as e:
            print(f"An unexpected error occurred: {e}")