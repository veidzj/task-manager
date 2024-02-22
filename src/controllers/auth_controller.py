from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from src.application.add_account import AddAccount
from src.repository.add_account_repository import AddAccountRepository
from src.application.authentication import Authentication
from src.repository.get_account_by_email_repository import GetAccountByEmailRepository
from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError
from src.domain.errors.validation_error import ValidationError

auth_blueprint = Blueprint('auth', __name__,)

MONGO_URI = 'mongodb://127.0.0.1:27017'
DB_NAME = 'task-manager'
SECRET_KEY = 'jwt-secret'

add_account_repository = AddAccountRepository(MONGO_URI, DB_NAME)
get_account_by_email_repository = GetAccountByEmailRepository(MONGO_URI, DB_NAME)
add_account_use_case = AddAccount(get_account_by_email_repository, add_account_repository)
authentication_use_case = Authentication(get_account_by_email_repository, SECRET_KEY)

@auth_blueprint.route('/v1/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        add_account_use_case.add(email, password)
        token = authentication_use_case.handle(email)
        return jsonify({
            'data': {
                'status': 201,
                'type': 'Authentication',
                'accessToken': token
            }
        }), 201
    except ValidationError as e:
         return jsonify({
            'error': {
                'status': 400,
                'type': 'Validation',
                'message': str(e)
            }
        }), 400
    except AccountAlreadyExistsError as e:
        return jsonify({
            'error': {
                'status': 401,
                'type': 'Authentication',
                'message': str(e)
            }
        }), 401
    except Exception as e:
        print(str(e))
        return jsonify({
            'error': {
                'status': 500,
                'type': 'Server',
                'message': 'Internal server error'
            }
        }), 500
