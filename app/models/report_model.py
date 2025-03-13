from datetime import datetime
from bson import ObjectId
from app.database import mongo
from datetime import timezone

def create_report(report_data):
    report_data['created_at'] = datetime.now(timezone.utc)
    report_data['updated_at'] = datetime.now(timezone.utc)
    return mongo.db.reports.insert_one(report_data).inserted_id

def get_report_by_id(report_id):
    report = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    if report:
        report["_id"] = str(report["_id"])  # Convert ObjectId to string
    return report

def update_report(report_id, update_data):
    update_data['updated_at'] = datetime.now(timezone.utc)
    mongo.db.reports.update_one({"_id": ObjectId(report_id)}, {"$set": update_data})

def delete_report(report_id):
    mongo.db.reports.delete_one({"_id": ObjectId(report_id)})

def list_reports():
    reports = list(mongo.db.reports.find())
    for report in reports:
        report["_id"] = str(report["_id"])  # Convert ObjectId to string
    return reports