from datetime import datetime
import uuid

class Account:
    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.createdAt = datetime.now()

        self.validate_password(self.password)

    def validate_password(self, password):
        if len(password) < 6 or len(password) > 255:
            raise ValueError('Password must be between 6 and 255 characters long')
