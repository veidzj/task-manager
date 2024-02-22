import pytest
from faker import Faker
from unittest.mock import Mock
import jwt
from werkzeug.security import generate_password_hash
from src.application.authentication import Authentication
from src.domain.errors.account_not_found_error import AccountNotFoundError
from src.domain.errors.invalid_credentials_error import InvalidCredentialsError

faker = Faker()
email = faker.email()
password = faker.password()

@pytest.fixture
def setup_sut():
    get_account_by_email_repository = Mock()
    secret_key = 'jwt_secret_key'
    sut = Authentication(get_account_by_email_repository, secret_key)
    return sut, get_account_by_email_repository, secret_key

def test_authentication_success(setup_sut):
    sut, get_account_by_email_repository, secret_key = setup_sut

    hashed_password = generate_password_hash(password)
    get_account_by_email_repository.get_by_email.return_value = {'email': email, 'password': hashed_password}

    token = sut.auth(email, password)

    decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])

    assert decoded_payload['email'] == email
    assert 'exp' in decoded_payload

def test_authentication_user_not_found(setup_sut):
    sut, get_account_by_email_repository, _ = setup_sut

    get_account_by_email_repository.get_by_email.return_value = None

    with pytest.raises(AccountNotFoundError):
        sut.auth(email, password)

def test_authentication_invalid_credentials(setup_sut):
    sut, get_account_by_email_repository, _ = setup_sut

    get_account_by_email_repository.get_by_email.return_value = {'email': email, 'password': password}

    with pytest.raises(InvalidCredentialsError):
        sut.auth(email, faker.password())

