import pytest
import mongomock
from faker import Faker
from src.repository.add_account_repository import AddAccountRepository

faker = Faker()

@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    yield client['test_db']

@pytest.fixture
def account_data():
    return {
        'email': faker.email(),
        'password': faker.password(),
    }

def test_add_account_success(mock_db, account_data):
    repository = AddAccountRepository('mongodb://localhost:27017', 'test_db')
    repository.db = mock_db

    repository.add(account_data)

    saved_account = mock_db.accounts.find_one({'email': account_data['email']})
    assert saved_account is not None
    assert saved_account['email'] == account_data['email']
    assert saved_account['password'] == account_data['password']
