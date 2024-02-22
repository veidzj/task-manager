import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from src.application.protocols.i_get_account_by_email_repository import IGetAccountByEmailRepository
from src.domain.errors.account_not_found_error import AccountNotFoundError
from src.domain.errors.invalid_credentials_error import InvalidCredentialsError

class Authentication:
    def __init__(self, get_account_by_email_repository: IGetAccountByEmailRepository, secret_key):
        self.get_account_by_email_repository = get_account_by_email_repository
        self.secret_key = secret_key

    def auth(self, email: str, password: str):
        user = self.get_account_by_email_repository.get_by_email(email)
        if not user:
            raise AccountNotFoundError()

        if not check_password_hash(user['password'], password):
            raise InvalidCredentialsError()

        payload = {
            'email': email,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        return token
