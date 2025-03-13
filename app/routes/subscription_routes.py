from flask import Blueprint, request, jsonify
from app.services.subscription_services import (
    create_subscription_service,
    get_subscription_by_id_service,
    update_subscription_service,
    delete_subscription_service,
    list_subscriptions_service
)
from app.schemas.subscription_schema import SubscriptionSchema
from marshmallow import ValidationError
from app.utils.decorators import token_required, admin_required

subscription_bp = Blueprint('subscription_bp', __name__)

# Admin creates a subscription plan 
@subscription_bp.route('/subscriptions', methods=['POST'])
@token_required
@admin_required
def create_subscription_route():
    try:
        subscription_data = SubscriptionSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        subscription_id = create_subscription_service(subscription_data)
        return jsonify({"id": str(subscription_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Everyone can view subscription plan details
@subscription_bp.route('/subscriptions/<subscription_id>', methods=['GET'])
@token_required
def get_subscription(subscription_id):
    try:
        subscription = get_subscription_by_id_service(subscription_id)
        if subscription:
            return jsonify(subscription), 200
        return jsonify({"error": "Subscription not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin updates subscription plan
@subscription_bp.route('/subscriptions/<subscription_id>', methods=['PUT'])
@token_required
@admin_required
def update_subscription_route(subscription_id):
    try:
        update_data = SubscriptionSchema().load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        update_subscription_service(subscription_id, update_data)
        return jsonify({"status": "updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin deletes subscription plan
@subscription_bp.route('/subscriptions/<subscription_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_subscription_route(subscription_id):
    try:
        delete_subscription_service(subscription_id)
        return jsonify({"status": "deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Everyone can view all available subscription plans
@subscription_bp.route('/subscriptions', methods=['GET'])
@token_required
def list_all_subscriptions():
    try:
        subscriptions = list_subscriptions_service()
        return jsonify(subscriptions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500