from flask import Blueprint, request, jsonify
from app.services.auth_services import (
    register_user_service,
    login_user_service,
    refresh_token_service,
    logout_service,
    verify_email_service,
    request_password_reset_service,
    reset_password_service
)
from app.extensions import limiter

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10 per hour")
def register():
    try:
        data = request.json
        response = register_user_service(data)
        status_code = response.get('status', 201)
        return jsonify({"success": True, "message": "Registration successful", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per 10 minutes")
def login():
    try:
        data = request.json
        response = login_user_service(data)
        status_code = response.get('status', 200)
        return jsonify({"success": True, "message": "Login successful", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/google-login', methods=['POST'])
@limiter.limit("10 per 10 minutes")
def google_login():
    try:
        data = request.json
        # response = google_login_service(data)
        # status_code = response.get('status', 200)
        return jsonify({"success": False, "message": "Google login not implemented"}), 501
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    try:
        refresh_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not refresh_token:
            return jsonify({"success": False, "message": "Refresh token missing"}), 400

        response = refresh_token_service(refresh_token)
        status_code = response.get('status', 200)
        return jsonify({"success": True, "message": "Token refreshed", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        refresh_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not refresh_token:
            return jsonify({"success": False, "message": "Refresh token missing"}), 400

        response = logout_service(refresh_token)
        status_code = response.get('status', 200)
        return jsonify({"success": True, "message": "Logged out", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({"success": False, "message": "Verification token missing"}), 400

        response = verify_email_service(token)
        status_code = response.get('status', 200)
        return jsonify({"success": True, "message": "Email verified", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/reset-password-request', methods=['POST'])
@limiter.limit("5 per hour")
def reset_password_request():
    try:
        email = request.json.get('email')
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400

        response = request_password_reset_service(email)
        status_code = response.get('status', 200)
        return jsonify({"success": True, "message": "Password reset email sent", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.json
        response = reset_password_service(data)
        status_code = response.get('status', 200)
        return jsonify({"success": True, "message": "Password reset successful", "data": response}), status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500