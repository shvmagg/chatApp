from datetime import datetime
from django.db import models
class Response:
    TYPE='websocket.send'
    def __init__(self,msgType):
        self.msgType=msgType

class SendMsgResponse(models.Model):
    msgType:models.CharField
    senderId:models.BigIntegerField
    msg:models.CharField
    def __init__(self, msg, senderId):
        # super.__init__("sm-send-msg")
        self.msgType="sm-send-msg"
        self.senderId=senderId
        self.msg=msg 

class MessageStatus(models.Model):
    senderId:models.BigIntegerField
    recieverId:models.BigIntegerField
    msgType:models.Model
    status:models.CharField
    timestamp:models.DateTimeField
    def __init__(self, senderId, recieverId):
        self.msgType="sm-message-status"
        self.senderId=senderId
        self.recieverId=recieverId
        self.status="sent"
        self.timestamp=datetime.now().timestamp()
        