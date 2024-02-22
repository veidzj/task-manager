class AccountNotFoundError(Exception):
    def __init__(self, message='Account not found'):
        self.message = message
        super().__init__(self.message)
