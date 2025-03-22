from flask import Blueprint, request
from app.services.report_services import (
    create_report_service,
    get_report_by_id_service,
    update_report_service,
    delete_report_service,
    list_reports_service
)
from app.schemas.report_schema import ReportSchema
from marshmallow import ValidationError
from app.utils.decorators import token_required, roles_required
from app.utils.responses import success_response, error_response

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/reports', methods=['POST'])
@roles_required(["premium", "admin"])
def create_report_route():
    current_user = request.user
    try:
        report_data = ReportSchema().load(request.json)
        report_data['user_id'] = str(current_user['_id'])

        report_id = create_report_service(report_data)
        return success_response("Report created", {"id": str(report_id)}, status_code=201)

    except ValidationError as err:
        return error_response(err.messages, status_code=400)
    except Exception as e:
        return error_response(str(e), status_code=500)

@report_bp.route('/reports/<report_id>', methods=['GET'])
@roles_required(["premium", "admin"])
def get_report(report_id):
    current_user = request.user
    try:
        report = get_report_by_id_service(report_id)
        if not report:
            return error_response("Report not found", status_code=404)

        if not current_user['is_admin'] and report['user_id'] != str(current_user['_id']):
            return error_response("Unauthorized", status_code=403)

        return success_response("Report fetched", report)

    except Exception as e:
        return error_response(str(e), status_code=500)

@report_bp.route('/reports/<report_id>', methods=['PUT'])
@roles_required(["premium", "admin"])
def update_report_route(report_id):
    current_user = request.user
    try:
        update_data = ReportSchema().load(request.json, partial=True)

        report = get_report_by_id_service(report_id)
        if not report:
            return error_response("Report not found", status_code=404)

        if not current_user['is_admin'] and report['user_id'] != str(current_user['_id']):
            return error_response("Unauthorized", status_code=403)

        update_report_service(report_id, update_data)
        return success_response("Report updated")

    except ValidationError as err:
        return error_response(err.messages, status_code=400)
    except Exception as e:
        return error_response(str(e), status_code=500)

@report_bp.route('/reports/<report_id>', methods=['DELETE'])
@roles_required(["premium", "admin"])
def delete_report_route(report_id):
    current_user = request.user
    try:
        report = get_report_by_id_service(report_id)
        if not report:
            return error_response("Report not found", status_code=404)

        if not current_user['is_admin'] and report['user_id'] != str(current_user['_id']):
            return error_response("Unauthorized", status_code=403)

        delete_report_service(report_id)
        return success_response("Report deleted")

    except Exception as e:
        return error_response(str(e), status_code=500)

@report_bp.route('/reports', methods=['GET'])
@roles_required(["premium", "admin"])
def list_all_reports():
    current_user = request.user
    try:
        if current_user['is_admin']:
            reports = list_reports_service()
        else:
            reports = list_reports_service(user_id=str(current_user['_id']))

        return success_response("Reports fetched", reports)

    except Exception as e:
        return error_response(str(e), status_code=500)