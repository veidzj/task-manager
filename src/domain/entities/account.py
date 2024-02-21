from datetime import datetime
import uuid

class Account:
    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.createdAt = datetime.now()
