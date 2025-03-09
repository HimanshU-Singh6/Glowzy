from app import create_app

flask_app = create_app()
# celery = celery_init_app(flask_app)

if __name__ == "__main__":
    flask_app.run(debug=True)