from app.database import mongo
from bson import ObjectId
from datetime import datetime

def create_report(user_id, report_data):
    report_data['user_id'] = ObjectId(user_id)
    report_data['created_at'] = datetime.utcnow()
    report_data['updated_at'] = datetime.utcnow()
    return mongo.db.reports.insert_one(report_data)

def get_report_by_id(report_id):
    return mongo.db.reports.find_one({"_id": ObjectId(report_id)})

def update_report(report_id, update_data):
    update_data['updated_at'] = datetime.utcnow()
    return mongo.db.reports.update_one({"_id": ObjectId(report_id)}, {"$set": update_data})

def delete_report(report_id):
    return mongo.db.reports.delete_one({"_id": ObjectId(report_id)})

def list_reports_by_user(user_id):
    return list(mongo.db.reports.find({"user_id": ObjectId(user_id)}))