class AccountAlreadyExistsError(Exception):
    def __init__(self, message='Account already exists'):
        self.message = message
        super().__init__(self.message)
