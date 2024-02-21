import pytest
import mongomock
from faker import Faker
from src.repository.add_account_repository import AddAccountRepository

faker = Faker()

@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    yield client['test_db']

def test_add_account_success(mock_db):
    repository = AddAccountRepository('mongodb://localhost:27017', 'test_db')
    repository.db = mock_db

    email = faker.email()
    password = faker.password()
    account_data = {'email': email, 'password': password}
    repository.add(account_data)

    saved_account = mock_db.accounts.find_one({'email': email})
    assert saved_account is not None
    assert saved_account['email'] == email
    assert saved_account['password'] == password
