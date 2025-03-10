from flask import Blueprint

# TODO: update this routes
# Import your blueprints from each route file
from .user_routes import user_bp
from .report_routes import report_bp
from .subscription_routes import subscription_bp

def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(report_bp, url_prefix='/api/v1')
    app.register_blueprint(subscription_bp, url_prefix='/api/v1')