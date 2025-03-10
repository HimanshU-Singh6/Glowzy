from app.models.subscription_model import (
    create_subscription as create_subscription_db,
    get_subscription_by_id as get_subscription_by_id_db,
    update_subscription as update_subscription_db,
    delete_subscription as delete_subscription_db,
    list_subscriptions as list_subscriptions_db
)

def create_subscription_service(subscription_data):
    return create_subscription_db(subscription_data)

def get_subscription_by_id_service(subscription_id):
    return get_subscription_by_id_db(subscription_id)

def update_subscription_service(subscription_id, update_data):
    return update_subscription_db(subscription_id, update_data)

def delete_subscription_service(subscription_id):
    return delete_subscription_db(subscription_id)

def list_subscriptions_service():
    return list_subscriptions_db()