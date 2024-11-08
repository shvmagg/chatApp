from django.db import models
class Request(models.Model):
    type:models.CharField
    text:models.CharField
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class AuthRequest(models.Model): #{"senderId":2,"msgType":"auth"}
    senderId:models.BigIntegerField
    msgType:models.CharField
    def __init__(self, senderId, msgType):
        self.senderId = senderId
        self.msgType = msgType
    
class LogOutRequest(models.Model): #{"senderId":2,"msgType":"auth"}
    senderId:models.BigIntegerField
    msgType:models.CharField
    def __init__(self, senderId):
        self.senderId=senderId
        self.msgType='logOut'

class SendMessageRequest(models.Model):
    recieverId:models.CharField
    #senderId:int
    msg:models.CharField
    msgType:models.CharField
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    #senderId=user.userId
    