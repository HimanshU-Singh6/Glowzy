from flask import Blueprint, request, jsonify
from app.services.user_services import (
    create_user_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
    list_users_service
)
from app.schemas.user_schema import UserSchema
from marshmallow import ValidationError
from app.utils.decorators import token_required, admin_required

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

@user_bp.route('/users', methods=['POST'])
def create_user_route():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "message": "Validation failed", "errors": err.messages}), 400

    try:
        user_id = create_user_service(user_data)
        print("user_id", user_id)
        return jsonify({"success": True, "data": {"id": str(user_id)}, "message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    current_user = request.user

    if current_user['role'] != 'admin' and current_user['user_id'] != user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    try:
        user = get_user_by_id_service(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        user_data = user_schema.dump(user)
        return jsonify({"success": True, "data": user_data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
@token_required
def update_user_route(user_id):
    current_user = request.user

    if current_user['role'] != 'admin' and current_user['user_id'] != user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    try:
        update_data = user_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"success": False, "message": "Validation failed", "errors": err.messages}), 400

    try:
        updated_user = update_user_service(user_id, update_data)
        if updated_user.modified_count == 0:
            return jsonify({"success": False, "message": "User not found or no changes applied"}), 404

        return jsonify({"success": True, "message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
@token_required
def delete_user_route(user_id):
    current_user = request.user

    if current_user['role'] != 'admin' and current_user['user_id'] != user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    try:
        deleted_user = delete_user_service(user_id)
        if deleted_user.deleted_count == 0:
            return jsonify({"success": False, "message": "User not found"}), 404

        return jsonify({"success": True, "message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/users', methods=['GET'])
@admin_required
def list_all_users():
    try:
        users = list_users_service()

        # Optional: implement pagination
        users_data = user_list_schema.dump(users)
        return jsonify({"success": True, "data": users_data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500