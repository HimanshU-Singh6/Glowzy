from flask_pymongo import PyMongo
from pymongo.errors import ServerSelectionTimeoutError


mongo = PyMongo()

def init_db(app):
    # Setup MongoDB with PyMongo
    mongo.init_app(app)

def get_users():
    users_collection = mongo.db.users
    return list(users_collection.find())

def add_user(user_data):
    users_collection = mongo.db.users
    return users_collection.insert_one(user_data)

def find_user_by_email(email):
    users_collection = mongo.db.users
    return users_collection.find_one({"email": email})

def check_connection():
    try:
        mongo.cx.server_info()
        return True, "Database is connected!"
    except ServerSelectionTimeoutError as e:
        return False, str(e)