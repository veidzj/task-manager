import pytest
from faker import Faker
from unittest.mock import Mock
from src.application.add_account import AddAccount
from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError

faker = Faker()
email = faker.email()
password = faker.password()

@pytest.fixture
def setup_sut():
    mock_get_account_by_email_repository = Mock()
    mock_add_account_repository = Mock()
    sut = AddAccount(mock_get_account_by_email_repository, mock_add_account_repository)
    return sut, mock_get_account_by_email_repository, mock_add_account_repository

def test_add_new_account_success(setup_sut):
    sut, mock_get_account_by_email_repository, mock_add_account_repository = setup_sut
    mock_get_account_by_email_repository.get_by_email.return_value = None

    sut.add(email, password)

    mock_add_account_repository.add.assert_called_once()
    hashed_password = mock_add_account_repository.add.call_args[0][0]['password']
    assert hashed_password != password

def test_add_account_fails_when_account_exists(setup_sut):
    sut, mock_get_account_by_email_repository, mock_add_account_repository = setup_sut

    mock_get_account_by_email_repository.get_by_email.return_value = {'email': email, 'password': password}

    with pytest.raises(AccountAlreadyExistsError):
        sut.add(email, password)

    mock_add_account_repository.add.assert_not_called()
