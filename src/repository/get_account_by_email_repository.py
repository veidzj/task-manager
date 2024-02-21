from pymongo import MongoClient

class GetAccountByEmailRepository:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_by_email(self, email):
        account = self.db.accounts.find_one({'email': email})
        return account
