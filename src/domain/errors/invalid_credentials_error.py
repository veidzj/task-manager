class InvalidCredentialsError(Exception):
    def __init__(self):
        self.message = 'Invalid credentials'
        super().__init__(self.message)
