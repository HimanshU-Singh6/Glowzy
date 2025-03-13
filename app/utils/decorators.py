from functools import wraps
from flask import request, jsonify
from jwt import ExpiredSignatureError
from app.utils.jwt_utils import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_parts = auth_header.split(" ")
            if len(token_parts) == 2 and token_parts[0] == 'Bearer':
                token = token_parts[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            payload = decode_token(token)
            request.user = {
                'user_id': payload['user_id'],
                'role': payload['role']
            }
        except ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401

        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)

    return decorated