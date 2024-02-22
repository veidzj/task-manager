from src.domain.entities.account import Account

class IGetAccountByEmailRepository:
    def get_by_email(self, email: str) -> Account:
        pass
