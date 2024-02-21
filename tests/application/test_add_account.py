import pytest
from faker import Faker
from unittest.mock import Mock
from werkzeug.security import generate_password_hash
from src.application.add_account import AddAccount
from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError

faker = Faker()
email = faker.email()
password = faker.password()

def test_add_new_account_success():
    mock_get_account_by_email_repository = Mock()
    mock_add_account_repository = Mock()
    mock_get_account_by_email_repository.get_by_email.return_value = None
    add_account = AddAccount(mock_get_account_by_email_repository, mock_add_account_repository)

    add_account.add(email, password)

    mock_add_account_repository.add.assert_called_once()
    hashed_password = mock_add_account_repository.add.call_args[0][0]['password']
    assert hashed_password != password

def test_add_account_fails_when_account_exists():
    mock_get_account_by_email_repository = Mock()
    mock_add_account_repository = Mock()

    mock_get_account_by_email_repository.get_by_email.return_value = {'email': email, 'password': password}

    add_account = AddAccount(mock_get_account_by_email_repository, mock_add_account_repository)

    with pytest.raises(AccountAlreadyExistsError):
        add_account.add(email, password)

    mock_add_account_repository.add.assert_not_called()
