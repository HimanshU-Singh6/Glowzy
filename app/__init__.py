from flask import Flask 
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from .database import init_db , check_connection
import os

jwt = JWTManager()

def create_app():
    load_dotenv() 

    # Initialize Flask app and configure the app with the configuration settings from config.py
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db(app)
    jwt.init_app(app)
    CORS(app)

    @app.route('/')
    def hello_world():
        return '<p>hello world!!</p>'
    
    @app.route('/check-db')
    def check_db():
        success, message = check_connection()
        status = "success" if success else "error"
        return {"status": status, "message": message}


    return app
