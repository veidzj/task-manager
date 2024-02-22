import pytest
import mongomock
from faker import Faker
from src.infra.repository.get_account_by_email_repository import GetAccountByEmailRepository

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
    sut = GetAccountByEmailRepository('mongodb://localhost:27017', 'test_db')
    sut.db = mock_db
    return sut, mock_db, account_data

def test_get_by_email_success(setup_sut):
    sut, mock_db, account_data = setup_sut

    mock_db.accounts.insert_one(account_data)

    found_account = sut.get_by_email(account_data['email'])
    assert found_account is not None
    assert found_account['email'] == account_data['email']
    assert found_account['password'] == account_data['password']
