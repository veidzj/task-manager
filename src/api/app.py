from flask import Flask
from src.controllers.health_check import health_check_blueprint
from src.controllers.auth_controller import auth_blueprint

app = Flask(__name__)

app.register_blueprint(health_check_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
