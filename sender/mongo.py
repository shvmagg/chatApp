"""
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['ChatApp']
collection = db['messages']

#recieverId='123'

#messages = [
#    {"content": "Hello!", "timestamp": "2024-10-10T10:00:00Z"},
#    {"content": "How are you?", "timestamp": "2024-10-10T10:01:00Z"},
#    {"content": "See you later!", "timestamp": "2024-10-10T10:02:00Z"}
#]
db.yourCollectionName.insertOne({
  "_id": 1,
  "msg": [
    {
      "msgType": "sm-send-msg",
      "senderId": 2,
      "msg": "hello"
    },
    {
      "msgType": "sm-send-msg",
      "senderId": 2,
      "msg": "hello"
    },
    {
      "msgType": "sm-send-msg",
      "senderId": 2,
      "msg": "hello"
    }
  ]
})

document = {
    "receiverId": receiver_id,
    "messages": messages  # Array of message objects
}

collection.insert_one(document)

result = collection.find_one({"receiverId": 1})
print(result)
"""