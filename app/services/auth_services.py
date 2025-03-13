from datetime import datetime
from bson import ObjectId
from flask import current_app
from app.services.user_services import (
    create_user_service,
    get_user_by_email_service,
    get_user_by_id_service,
    update_user_service
)
from datetime import datetime, timezone
from app.utils.password_utils import hash_password, check_password
from app.utils.jwt_utils import generate_access_token, generate_refresh_token, decode_token


# TODO: DO THIS LATER
# Commented out blacklist and email features for now
# from app.models.blacklist_model import add_to_blacklist, is_token_blacklisted
# from app.utils.email_utils import (
#     send_verification_email,
#     send_password_reset_email
# )

def register_user_service(data):
    # TODO: we can add name registration and profile pic later
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"error": "Email and password are required", "status": 400}

    existing_user = get_user_by_email_service(email)
    if existing_user:
        return {"error": "User already exists", "status": 400}

    hashed_pw = hash_password(password)
    user_data = {
        "email": email,
        "password": hashed_pw,
        "is_verified": False,
        "role": "user",
        "created_at": datetime.now(timezone.utc)
    }

    user = create_user_service(user_data)

    # Commented out email verification for now
    # send_verification_email(user)

    return {"message": "User registered successfully.", "status": 201}

def login_user_service(data):
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"error": "Email and password are required", "status": 400}

    user = get_user_by_email_service(email)
    if not user:
        return {"error": "Invalid email or password", "status": 401}

    if not check_password(password, user['password']):
        return {"error": "Invalid email or password", "status": 401}

    # Comment out if you don't want to enforce email verification for now
    # if not user.get('is_verified'):
    #     return {"error": "Email not verified", "status": 401}

    access_token = generate_access_token(str(user['_id']), user['role'])
    refresh_token = generate_refresh_token(str(user['_id']))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": str(user['_id']),
            "email": user['email'],
            "role": user['role']
        }
    }

def refresh_token_service(refresh_token):
    if not refresh_token:
        return {"error": "Refresh token required", "status": 401}

    # if is_token_blacklisted(refresh_token):
    #     return {"error": "Invalid or expired token", "status": 401}

    try:
        payload = decode_token(refresh_token, refresh=True)
        user_id = payload['user_id']
        user = get_user_by_id_service(ObjectId(user_id))

        if not user:
            return {"error": "User not found", "status": 404}

        new_access_token = generate_access_token(str(user['_id']), user['role'])
        return {"access_token": new_access_token}

    except Exception as e:
        return {"error": str(e), "status": 401}

def logout_service(refresh_token):
    if not refresh_token:
        return {"error": "Refresh token required", "status": 400}

    # if is_token_blacklisted(refresh_token):
    #     return {"error": "Token already invalidated", "status": 400}

    try:
        decode_token(refresh_token, refresh=True)

        # add_to_blacklist(refresh_token)

        return {"message": "Logged out successfully"}

    except Exception as e:
        return {"error": str(e), "status": 400}

def verify_email_service(token):
    try:
        payload = decode_token(token)
        user_id = payload.get('user_id')

        user = get_user_by_id_service(ObjectId(user_id))
        if not user:
            return {"error": "User not found", "status": 404}

        if user.get('is_verified'):
            return {"message": "Email already verified"}

        update_user_service(ObjectId(user_id), {'is_verified': True})

        return {"message": "Email verified successfully"}

    except Exception as e:
        return {"error": str(e), "status": 400}

def request_password_reset_service(email):
    user = get_user_by_email_service(email)
    if not user:
        return {"error": "User not found", "status": 404}

    reset_token = generate_access_token(str(user['_id']), user['role'])

    # send_password_reset_email(user, reset_token)

    return {"message": "Password reset token generated (email sending skipped for now)."}

def reset_password_service(data):
    token = data.get('token')
    new_password = data.get('password')

    if not token or not new_password:
        return {"error": "Token and new password are required", "status": 400}

    try:
        payload = decode_token(token)
        user_id = payload.get('user_id')

        hashed_pw = hash_password(new_password)
        update_user_service(ObjectId(user_id), {'password': hashed_pw})

        return {"message": "Password has been reset successfully"}

    except Exception as e:
        return {"error": str(e), "status": 400}

# Optional Google OAuth Service (commented)
# def google_login_service(data):
#     id_token = data.get('id_token')
#     if not id_token:
#         return {"error": "Missing ID token", "status": 400}
#     try:
#         result = google_oauth_login(id_token)
#         return result
#     except Exception as e:
#         return {"error": str(e), "status": 400}