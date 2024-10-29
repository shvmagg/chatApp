class Response:
    TYPE='websocket.send'
    def __init__(self,msgType):
        self.msgType=msgType

class SendMsgResponse:
    msgType:str
    senderId:int
    msg:str
    def __init__(self, msg, senderId):
        # super.__init__("sm-send-msg")
        self.msgType="sm-send-msg"
        self.senderId=senderId
        self.msg=msg 