from flask import Flask
from src.controllers.health_check import health_check_blueprint

app = Flask(__name__)

app.register_blueprint(health_check_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
