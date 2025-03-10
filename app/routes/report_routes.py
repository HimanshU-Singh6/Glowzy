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

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/reports', methods=['POST'])
def create_report_route():
    try:
        report_data = ReportSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        report_id = create_report_service(report_data)
        return jsonify({"id": str(report_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    try:
        report = get_report_by_id_service(report_id)
        if report:
            return jsonify(report), 200
        return jsonify({"error": "Report not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports/<report_id>', methods=['PUT'])
def update_report_route(report_id):
    try:
        update_data = ReportSchema().load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        update_report_service(report_id, update_data)
        return jsonify({"status": "updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports/<report_id>', methods=['DELETE'])
def delete_report_route(report_id):
    try:
        delete_report_service(report_id)
        return jsonify({"status": "deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/reports', methods=['GET'])
def list_all_reports():
    try:
        reports = list_reports_service()
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500