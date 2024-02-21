import pytest
from datetime import datetime
from uuid import UUID
from faker import Faker
from src.domain.entities.account import Account

faker = Faker()

def test_account_creation():
    email = faker.email()
    password = faker.password()    
    account = Account(email, password)

    assert account.email == email
    assert account.password == password
    assert isinstance(account.id, UUID)
    assert isinstance(account.createdAt, datetime)

def test_invalid_password():
    with pytest.raises(ValueError):
        Account(faker.email(), faker.pystr(1, 5))
    with pytest.raises(ValueError):
        Account(faker.email(), faker.pystr(256, 257))
