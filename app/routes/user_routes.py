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

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user_route():
    try:
        # Validate and deserialize input data
        user_data = UserSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error1": err.messages}), 400

    try:
        # Call the service layer to create a user
        user_id = create_user_service(user_data)
        return jsonify({"id": str(user_id)}), 201
    except Exception as e:
        return jsonify({"error2": str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_by_id_service(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    try:
        # Validate and deserialize input data
        update_data = UserSchema().load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        update_user_service(user_id, update_data)
        return jsonify({"status": "updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    try:
        delete_user_service(user_id)
        return jsonify({"status": "deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users', methods=['GET'])
def list_all_users():
    try:
        users = list_users_service()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500