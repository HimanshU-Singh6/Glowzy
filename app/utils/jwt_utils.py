import jwt
from datetime import datetime, timedelta
from flask import current_app
from datetime import datetime, timezone

def generate_access_token(user_id, role):
    payload = {
        'user_id': str(user_id),
        'role': role,
        'is_admin': role == 'admin',
        'exp': datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def generate_refresh_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(days=7)  # Refresh token expires in 7 days
    }
    token = jwt.encode(payload, current_app.config['JWT_REFRESH_SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token, refresh=False):
    secret = current_app.config['JWT_REFRESH_SECRET_KEY'] if refresh else current_app.config['JWT_SECRET_KEY']
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')