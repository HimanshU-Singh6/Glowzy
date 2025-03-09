from app.database import mongo
from bson import ObjectId
from datetime import datetime

def create_user(user_data):
    user_data['created_at'] = datetime.utcnow()
    user_data['updated_at'] = datetime.utcnow()
    return mongo.db.users.insert_one(user_data)

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def update_user(user_id, update_data):
    update_data['updated_at'] = datetime.utcnow()
    return mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

def delete_user(user_id):
    return mongo.db.users.delete_one({"_id": ObjectId(user_id)})

def list_users():
    return list(mongo.db.users.find())