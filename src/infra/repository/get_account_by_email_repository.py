from pymongo import MongoClient
from src.application.protocols.i_get_account_by_email_repository import IGetAccountByEmailRepository

class GetAccountByEmailRepository(IGetAccountByEmailRepository):
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_by_email(self, email):
        account = self.db.accounts.find_one({'email': email})
        return account
