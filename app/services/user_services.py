from app.models.user_model import (
    create_user as create_user_db,
    get_user_by_id as get_user_by_id_db,
    update_user as update_user_db,
    delete_user as delete_user_db,
    list_users as list_users_db
)

def create_user_service(user_data):
    return create_user_db(user_data)

def get_user_by_id_service(user_id):
    return get_user_by_id_db(user_id)

def update_user_service(user_id, update_data):
    return update_user_db(user_id, update_data)

def delete_user_service(user_id):
    return delete_user_db(user_id)

def list_users_service():
    return list_users_db()