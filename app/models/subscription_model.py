from app.database import mongo
from bson import ObjectId
from datetime import datetime

def create_subscription(user_id, subscription_data):
    subscription_data['user_id'] = ObjectId(user_id)
    subscription_data['start_date'] = datetime.utcnow()
    subscription_data['end_date'] = subscription_data.get('end_date')
    subscription_data['is_active'] = True
    return mongo.db.subscriptions.insert_one(subscription_data)

def get_subscription_by_user(user_id):
    return mongo.db.subscriptions.find_one({"user_id": ObjectId(user_id)})

def cancel_subscription(user_id):
    return mongo.db.subscriptions.update_one(
        {"user_id": ObjectId(user_id)},
        {"$set": {"is_active": False, "end_date": datetime.utcnow()}}
    )