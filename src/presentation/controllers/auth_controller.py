from flask import Blueprint, request, jsonify
from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError
from src.domain.errors.invalid_credentials_error import InvalidCredentialsError
from src.domain.errors.account_not_found_error import AccountNotFoundError
from src.domain.errors.validation_error import ValidationError
from src.application.add_account import AddAccount
from src.application.authentication import Authentication
from src.infra.repository.add_account_repository import AddAccountRepository
from src.infra.repository.get_account_by_email_repository import GetAccountByEmailRepository

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
        token = authentication_use_case.auth(email, password)
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
    except InvalidCredentialsError as e:
        return jsonify({
            'error': {
                'status': 401,
                'type': 'Authentication',
                'message': str(e)
            }
        }), 401
    except AccountNotFoundError as e:
        return jsonify({
            'error': {
                'status': 404,
                'type': 'Authentication',
                'message': str(e)
            }
        }), 404
    except Exception as e:
        return jsonify({
            'error': {
                'status': 500,
                'type': 'Server',
                'message': 'Internal server error'
            }
        }), 500

@auth_blueprint.route('/v1/sign-in', methods=['POST'])
def sign_in():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        token = authentication_use_case.auth(email, password)
        return jsonify({
            'data': {
                'status': 200,
                'type': 'Authentication',
                'accessToken': token
            }
        }), 200
    except InvalidCredentialsError as e:
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
