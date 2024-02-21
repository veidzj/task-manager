from flask import Flask
from src.controllers.health_check import health_check_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(health_check_blueprint)
    return app

def test_health_check():
    app = create_app()
    client = app.test_client()
    response = client.get('/v1/health')
    assert response.status_code == 200
