# Create your models here.

class User:
    userId:int
    send:any
    def __init__(self,send,userId):
        self.send=send
        self.userId=userId
