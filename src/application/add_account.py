from werkzeug.security import generate_password_hash
from src.application.protocols.i_get_account_by_email_repository import IGetAccountByEmailRepository
from src.application.protocols.i_add_account_repository import IAddAccountRepository
from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError

class AddAccount:
    def __init__(self, get_account_by_email_repository: IGetAccountByEmailRepository, add_account_repository: IAddAccountRepository):
        self.get_account_by_email_repository = get_account_by_email_repository
        self.add_account_repository = add_account_repository

    def add(self, email: str, password: str):
        account = self.get_account_by_email_repository.get_by_email(email)
        if account:
            raise AccountAlreadyExistsError()
        hashed_password = generate_password_hash(password)
        account_data = {"email": email, "password": hashed_password}
        self.add_account_repository.add(account_data)
