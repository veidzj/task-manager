import pytest
import mongomock
from faker import Faker
from src.repository.get_account_by_email_repository import GetAccountByEmailRepository

faker = Faker()

@pytest.fixture
def mock_db():
    with mongomock.MongoClient() as client:
        yield client['test_db']

def test_get_by_email_success(mock_db):
    repository = GetAccountByEmailRepository('mongodb://localhost:27017', 'test_db')
    repository.db = mock_db

    email = faker.email()
    password = faker.password()
    account_data = {'email': email, 'password': password}
    mock_db.accounts.insert_one(account_data)

    found_account = repository.get_by_email(account_data['email'])
    assert found_account is not None
    assert found_account['email'] == account_data['email']
    assert found_account['password'] == account_data['password']
