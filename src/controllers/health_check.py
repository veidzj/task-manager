from flask import Blueprint

health_check_blueprint = Blueprint('health_check', __name__)

@health_check_blueprint.route('/v1/health', methods=['GET'])
def health_check():
    return '', 200
