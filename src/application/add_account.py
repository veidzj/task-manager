from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError
from werkzeug.security import generate_password_hash

class AddAccount:
    def __init__(self, get_account_by_email_repository, add_account_repository):
        self.get_account_by_email_repository = get_account_by_email_repository
        self.add_account_repository = add_account_repository

    def add(self, email: str, password: str):
        account = self.get_account_by_email_repository.get_by_email(email)
        if account:
            raise AccountAlreadyExistsError()
        hashed_password = generate_password_hash(password)
        account_data = {"email": email, "password": hashed_password}
        self.add_account_repository.add(account_data)
