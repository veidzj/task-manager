import jwt
from datetime import datetime, timedelta
from src.domain.errors.account_not_found_error import AccountNotFoundError

class Authentication:
    def __init__(self, user_repository, secret_key):
        self.user_repository = user_repository
        self.secret_key = secret_key

    def handle(self, email: str):
        user = self.user_repository.get_by_email(email)
        if not user:
            raise AccountNotFoundError()

        payload = {
            'email': email,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        return token
