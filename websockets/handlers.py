#sending message
from threading import Thread
import asyncio
import json
# from response_models import SendMsgResponse
# from websockets import serializers
from websockets.models import User
from websockets.request_models import LogOutRequest, SendMessageRequest
from websockets.response_models import SendMsgResponse
#from websockets.models import User
#from collections import namedtuple
from pymongo import MongoClient
from pymongo.errors import PyMongoError


client = MongoClient('mongodb://localhost:27017/')
db = client['chatApp']
collection = db['messages']

ids = {}
store={} #{ run mongod->  mongod --dbpath=/Users/shivamaggarwal/data/db 
         #recieverId:[{msg},{msg},{msg}]
         #}

def getUser(userid) -> User:
    return ids.get(userid, None)


def setUser(userid, user:User):
    ids[userid] = user

def removeUser(userId):
    ids.pop(userId)

# Function to watch for changes
def watch_new_messages():
    try:
        # Start watching the collection for new changes
        with collection.watch() as stream:
            print("Watching for changes...")
            for change in stream:
                # Print the change details (you can process it as needed)
                print("Trying to print change")
                print(f"Change detected: {change}")
                operationType=change.get('operationType')
                if operationType=='insert':
                    print("performing insert operation")
                    full_doc=change.get('fullDocument')
                    recieverId=full_doc.get('_id')
                    syncMsg(recieverId)
                    # if msgs:
                    #     recieverId=full_doc.get('_id')
                    #     user = getUser(recieverId)
                    #     new_thread = Thread(target=sendMessage,args = (user,msg[0],))
                    #     new_thread.start()
                    # else:
                    #     print("no message in watch_new_messages")
                    
                    print("insert message implemented")
                elif operationType=='update':
                    print("performing update operation")
                    docKey=change.get('documentKey')
                    recieverId=docKey.get('_id')
                    user=getUser(recieverId)
                    if user:
                        syncMsg(recieverId)
                    else:
                        print("user currently offline")
                elif operationType=='delete':
                    print("A message has been removed")
                
                
    except PyMongoError as e:
        print(f"An error occurred: {e}")


def myHandler(type, data, senderId):#from , to, message, msg_type
    match type:
        case 'send_msg':
            return handleSendMsg(data, senderId)#{"recieverId":2,"msg":"hello","msgType":"send_msg"}
        case 'logOut':
            return handleOffline(senderId) #data->userId(to be removed),msg_type
        case _:
            return handelDefault(data, senderId)
        

#Handling defalt case
def handelDefault(data, senderId):
    return {'staus':'unknown'}


#sync messages
def syncMsg(recieverId):
    result = collection.find_one_and_delete({"_id": recieverId})
    #print("result->",result)
    if result:
        for doc in result:
            print(doc)
        msgs=result.get("msg",[])
        print("msgs:",msgs)
        user = getUser(recieverId)
        new_thread = Thread(target=syncMessage,args = (user,msgs,))
        new_thread.start()
        new_thread.join()#waiting for the thread execution
        #collection.delete_one({"_id":recieverId})

    """if recieverId in store:
        user = getUser(recieverId)
        msgs=store[recieverId]
        new_thread = Thread(target=syncMessage,args = (user,msgs,))
        new_thread.start()
    """    
def syncMessage(user:User,msgs):
    i=0
    print(len(msgs))
    while i<len(msgs):
        sendMessage(user,msgs[i])
        i+=1


#Handling send message
def handleSendMsg(data, senderId):
    cm = SendMessageRequest(**data)#{"recieverId":2,"msg":"hello","msgType":"send_msg"}
    sm = SendMsgResponse(cm.msg,senderId)#message,msgType
    jsonMsg = json.dumps(sm.__dict__)
    print("msg:- ", jsonMsg)

    storeMsg(cm.recieverId, jsonMsg)


"""#def sendMsg(recieverId,data):#recieverId, {"msgType": "sm-send-msg", "senderId": 1, "msg": "Hello"}
    print(50)
    user = getUser(recieverId)
    print(52)
    storeMsg(recieverId,data)
    if user is None:
        storeMsg(recieverId,data)#recieving user and message to be recieved which contains {"msgType": "sm-send-msg", "senderId": 1, "msg": "Hello"}
        print(store)
    else:    
        new_thread = Thread(target=sendMessage,args = (user,data,))
        new_thread.start()
        #return sendMessage(data['to'],data)
"""


def sendMessage(user:User,msg:str):
    print("msg->",msg)
    print("user->",user)
    print(type(msg))
    if user is None:
        return {'status':'Offline'}
    reciever = getUser(user.userId)
    if reciever:
        try:
            asyncio.run(
                user.send({ #we are gettting send method via ids[userId] which we added in the auth method and we are sending message to the user using this.
                    'type': 'websocket.send',
                    'text': msg
                })
            )
            # collection.delete_one({"_id":user.userId})
            # {'status': 'Online'}
        except Exception as e:
            print("An exception occurred in sendMessage:", e)
            print("Exception type:", type(e).__name__)
            raise TypeError ('Failed to send message')
    else:
        print("User offline right now")


def storeMsg(recieverId,data):
    """if recieverId not in store:
        store.update({recieverId:[data]})
        print("store->",store)
    else:
        store[recieverId].append(data)
        print("store->",store)
""" 
    print("recieverId->",recieverId)
    check = {
        "_id":recieverId
    }
    try:
        collection.update_one(check, {"$push":{"msg":data}},upsert=True)
        # entry=collection.find_one(check)
        # if entry is not None:
        #     print("entry->",entry)
        # fill=collection.update_one(check, {"$push":{"msg":data}},upsert=True)
        # print("Matched count:", fill.matched_count)
        # print("Modified count:", fill.modified_count)
        # if fill.modified_count > 0:
        #     print("New message added.")
        # else:
        #     print("No documents were updated.")
        # else:
        #     print("in db else")
        #     msg={
        #         "_id":recieverId,
        #         "msg":[data]
        #     }
        #     collection.insert_one(msg)
        #     """client.close()"""
    except Exception as e:
        print("db error->",e)

#remove offline users from ids
def handleOffline(senderId):#user to be removed
    #print("data->",data)
    print("ids->",ids)
    cm=LogOutRequest(senderId)
    try:
        removeUser(cm.senderId)
        # {'status':'User offline'}
    except:        
        print("No such senderId exists in ids")
        # {'status':'Already Offline'}
    print("ids->",ids)
    