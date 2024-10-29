class Request:
    type:str
    text:str
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class AuthRequest: #{"senderId":2,"msgType":"auth"}
    senderId:int
    msgType:str
    def __init__(self, senderId, msgType):
        self.senderId = senderId
        self.msgType = msgType
    
class LogOutRequest: #{"senderId":2,"msgType":"auth"}
    senderId:int
    msgType:str
    def __init__(self, senderId):
        self.senderId=senderId
        self.msgType='logOut'

class SendMessageRequest:
    recieverId:int
    #senderId:int
    msg:str
    msgType:str
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    #senderId=user.userId
    