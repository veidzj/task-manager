from pymongo import MongoClient

class AddAccountRepository():
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def add(self, account_data):
        self.db.accounts.insert_one(account_data)
