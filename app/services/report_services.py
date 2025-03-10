from app.models.report_model import (
    create_report as create_report_db,
    get_report_by_id as get_report_by_id_db,
    update_report as update_report_db,
    delete_report as delete_report_db,
    list_reports as list_reports_db
)

def create_report_service(report_data):
    return create_report_db(report_data)

def get_report_by_id_service(report_id):
    return get_report_by_id_db(report_id)

def update_report_service(report_id, update_data):
    return update_report_db(report_id, update_data)

def delete_report_service(report_id):
    return delete_report_db(report_id)

def list_reports_service():
    return list_reports_db()