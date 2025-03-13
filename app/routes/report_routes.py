from flask import Blueprint, request, jsonify
from app.services.report_services import (
    create_report_service,
    get_report_by_id_service,
    update_report_service,
    delete_report_service,
    list_reports_service
)
from app.schemas.report_schema import ReportSchema
from marshmallow import ValidationError
from app.utils.decorators import token_required, admin_required

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/reports', methods=['POST'])
@token_required
def create_report_route():
    current_user = request.user
    try:
        report_data = ReportSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        # Inject user_id so we know who owns the report
        report_data['user_id'] = str(current_user['_id'])
        report_id = create_report_service(report_data)
        return jsonify({"id": str(report_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports/<report_id>', methods=['GET'])
@token_required
def get_report(report_id):
    current_user = request.user
    try:
        report = get_report_by_id_service(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404

        # Only allow user to access their own reports unless admin
        if not current_user['is_admin'] and report['user_id'] != str(current_user['_id']):
            return jsonify({"error": "Unauthorized"}), 403

        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports/<report_id>', methods=['PUT'])
@token_required
def update_report_route(report_id):
    current_user = request.user
    try:
        update_data = ReportSchema().load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        report = get_report_by_id_service(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404

        # Ownership check
        if not current_user['is_admin'] and report['user_id'] != str(current_user['_id']):
            return jsonify({"error": "Unauthorized"}), 403

        update_report_service(report_id, update_data)
        return jsonify({"status": "updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports/<report_id>', methods=['DELETE'])
@token_required
def delete_report_route(report_id):
    current_user = request.user
    try:
        report = get_report_by_id_service(report_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404

        if not current_user['is_admin'] and report['user_id'] != str(current_user['_id']):
            return jsonify({"error": "Unauthorized"}), 403

        delete_report_service(report_id)
        return jsonify({"status": "deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports', methods=['GET'])
@token_required
def list_all_reports():
    current_user = request.user
    try:
        if current_user['is_admin']:
            # Admins see all reports
            reports = list_reports_service()
        else:
            # Users see only their reports
            reports = list_reports_service(user_id=str(current_user['_id']))

        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500