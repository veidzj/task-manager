from datetime import datetime
import uuid
import re

class Account:
    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.createdAt = datetime.now()

        self.validate_email(self.email)
        self.validate_password(self.password)

    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Email must be a valid email')

    def validate_password(self, password):
        if len(password) < 6 or len(password) > 255:
            raise ValueError('Password must be between 6 and 255 characters long')
