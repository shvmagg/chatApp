import threading
from websockets.handlers import watch_new_messages
from websockets.models import User
from websockets.handlers import setUser, syncMsg
from websockets.request_models import AuthRequest

#problem with auth-> multiple devices can authenticate with same senderId
def handleAuth(data,send):#{"senderId":1,"msgType":"auth"},Address
    cm=AuthRequest(**data)#{"senderId":2,"msgType":"auth"}
    #print(type(send))
    user=User(send,cm.senderId)
    setUser(cm.senderId, user)
    syncMsg(cm.senderId)
    return user
    # {'status':'success'}