from app.database import mongo
from bson import ObjectId
from datetime import datetime, timezone

def create_user(user_data):
    user_data['created_at'] = datetime.now(timezone.utc)
    user_data['updated_at'] = datetime.now(timezone.utc)
    return mongo.db.users.insert_one(user_data)

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def update_user(user_id, update_data):
    update_data['updated_at'] = datetime.now(timezone.utc)
    return mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

def delete_user(user_id):
    return mongo.db.users.delete_one({"_id": ObjectId(user_id)})

def list_users(page=1, per_page=10):
    skips = per_page * (page - 1)
    users_cursor = mongo.db.users.find().skip(skips).limit(per_page)
    users = list(users_cursor)
    for user in users:
        user['_id'] = str(user['_id'])
        user.pop('password_hash', None)  # Remove sensitive data
    return users