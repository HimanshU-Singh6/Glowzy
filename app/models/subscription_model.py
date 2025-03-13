from datetime import datetime
from bson import ObjectId
from app.database import mongo
from datetime import timezone

def create_subscription(subscription_data):
    subscription_data['created_at'] = datetime.now(timezone.utc)
    subscription_data['updated_at'] = datetime.now(timezone.utc)
    return mongo.db.subscriptions.insert_one(subscription_data).inserted_id

def get_subscription_by_id(subscription_id):
    subscription = mongo.db.subscriptions.find_one({"_id": ObjectId(subscription_id)})
    if subscription:
        subscription["_id"] = str(subscription["_id"])  # Convert ObjectId to string
    return subscription

def update_subscription(subscription_id, update_data):
    update_data['updated_at'] = datetime.now(timezone.utc)
    mongo.db.subscriptions.update_one({"_id": ObjectId(subscription_id)}, {"$set": update_data})

def delete_subscription(subscription_id):
    mongo.db.subscriptions.delete_one({"_id": ObjectId(subscription_id)})

def list_subscriptions():
    subscriptions = list(mongo.db.subscriptions.find())
    for subscription in subscriptions:
        subscription["_id"] = str(subscription["_id"])  # Convert ObjectId to string
    return subscriptions