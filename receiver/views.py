# from django.shortcuts import render
# from pymongo import MongoClient
# from pymongo.errors import PyMongoError

# from sender.handlers import getUser, syncMsg

# # Create your views here.
# ids={}
# client = MongoClient('mongodb://localhost:27017/')
# db = client['chatApp']
# collection = db['messages']


# def removeUser(userId):
#     ids.pop(userId)

# async def watch_new_messages():
#     try:
#         # Start watching the collection for new changes
#         with collection.watch() as stream:
#             print("Watching for changes...")
#             for change in stream:
#                 # Print the change details (you can process it as needed)
#                 print("Trying to print change")
#                 print(f"Change detected: {change}")
#                 operationType=change.get('operationType')
#                 if operationType=='insert':
#                     print("performing insert operation")
#                     full_doc=change.get('fullDocument')
#                     recieverId=full_doc.get('_id')
#                     syncMsg(recieverId)
#                     # if msgs:
#                     #     recieverId=full_doc.get('_id')
#                     #     user = getUser(recieverId)
#                     #     new_thread = Thread(target=sendMessage,args = (user,msg[0],))
#                     #     new_thread.start()
#                     # else:
#                     #     print("no message in watch_new_messages")
                    
#                     print("insert message implemented")
#                 elif operationType=='update':
#                     print("performing update operation")
#                     docKey=change.get('documentKey')
#                     recieverId=docKey.get('_id')
#                     user=getUser(recieverId)
#                     if user:
#                         syncMsg(recieverId)
#                     else:
#                         print("user currently offline")
#                 elif operationType=='delete':
#                     print("A message has been removed")
                
#     except PyMongoError as e:
#         print(f"An error occurred: {e}")


# async def start_watch():
#     print("Start watch executed")
#     await watch_new_messages()