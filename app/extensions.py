from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient

cors = CORS()
limiter = Limiter(key_func=get_remote_address)

mongo_client = None
db = None

def init_extensions(app):
    cors.init_app(app)
    limiter.init_app(app)
    
    global mongo_client, db

    mongo_uri = app.config.get('MONGO_URI')
    mongo_dbname = app.config.get('MONGO_DBNAME')

    if not mongo_uri or not mongo_dbname:
        raise ValueError('MONGO_URI and MONGO_DBNAME must be set in app config')

    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[mongo_dbname]