import pytest
import mongomock
from faker import Faker
from src.infra.repository.add_account_repository import AddAccountRepository

faker = Faker()

@pytest.fixture
def mock_db():
    with mongomock.MongoClient() as client:
        yield client['test_db']

@pytest.fixture
def account_data():
    return {
        'email': faker.email(),
        'password': faker.password(),
    }

@pytest.fixture
def setup_sut(mock_db, account_data):
    sut = AddAccountRepository('mongodb://localhost:27017', 'test_db')
    sut.db = mock_db
    return sut, mock_db, account_data

def test_add_account_success(setup_sut):
    sut, mock_db, account_data = setup_sut

    sut.add(account_data)

    saved_account = mock_db.accounts.find_one({'email': account_data['email']})
    assert saved_account is not None
    assert saved_account['email'] == account_data['email']
    assert saved_account['password'] == account_data['password']
