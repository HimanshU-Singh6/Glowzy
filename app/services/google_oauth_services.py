# import os
# import requests
# from app.services.user_services import get_user_by_email_service, create_user_service
# from app.utils.password_utils import generate_random_password
# from app.utils.jwt_utils import create_access_token, create_refresh_token
# from app.config import Config
# GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID

# TODO: do this file after frontend completed


# def verify_google_token(id_token):
#     url = "https://oauth2.googleapis.com/tokeninfo"
#     response = requests.get(url, params={"id_token": id_token})

#     if response.status_code != 200:
#         raise Exception("Invalid Google token")

#     data = response.json()

#     # Verify the token audience
#     if data.get("aud") != GOOGLE_CLIENT_ID:
#         raise Exception("Token audience mismatch")

#     return data

# def google_oauth_login(id_token):
#     google_data = verify_google_token(id_token)

#     email = google_data.get("email")
#     if not email:
#         raise Exception("Google account email not found")

#     user = get_user_by_email_service(email)
#     if not user:
#         user_data = {
#             "email": email,
#             "password": generate_random_password(),
#             "is_verified": True,
#             "role": "user"
#         }

#         create_user_service(user_data)
#         user = get_user_by_email_service(email)

#     access_token = create_access_token({"user_id": str(user['_id']), "role": user['role']})
#     refresh_token = create_refresh_token({"user_id": str(user['_id'])})

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "user": {
#             "email": user['email'],
#             "role": user['role']
#         }
#     }