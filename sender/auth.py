import threading
from sender.handlers import watch_new_messages
from sender.models import User
from sender.handlers import setUser, syncMsg
from sender.request_models import AuthRequest

#problem with auth-> multiple devices can authenticate with same senderId
def handleAuth(data,send):#{"senderId":1,"msgType":"auth"},Address
    cm=AuthRequest(**data)#{"senderId":2,"msgType":"auth"}
    #print(type(send))
    user=User(send,cm.senderId)
    setUser(cm.senderId, user)
    syncMsg(cm.senderId)
    return user
    # {'status':'success'}