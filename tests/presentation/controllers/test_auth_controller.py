import pytest
from faker import Faker
from src.api.app import app
from unittest.mock import patch
from src.domain.errors.validation_error import ValidationError
from src.domain.errors.account_already_exists_error import AccountAlreadyExistsError
from src.domain.errors.invalid_credentials_error import InvalidCredentialsError
from src.domain.errors.account_not_found_error import AccountNotFoundError

faker = Faker()
email = faker.email()
password = faker.password()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sign_up_success(client):
    with patch('src.application.add_account.AddAccount.add') as mock_add_account, \
         patch('src.application.authentication.Authentication.auth') as mock_authentication:
        mock_add_account.return_value = None
        mock_authentication.return_value = faker.words()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 201
        assert 'accessToken' in response.json['data']

def test_sign_up_validation_error(client):
    with patch('src.application.add_account.AddAccount.add') as mock_add_account:
        mock_add_account.side_effect = ValidationError(faker.words())
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 400

def test_sign_up_account_already_exists_error(client):
    with patch('src.application.authentication.Authentication.auth') as mock_authentication:
        mock_authentication.side_effect = AccountAlreadyExistsError()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 401

def test_sign_up_invalid_credentials_error(client):
    with patch('src.application.authentication.Authentication.auth') as mock_authentication:
        mock_authentication.side_effect = InvalidCredentialsError()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 401

def test_sign_up_account_not_found_error(client):
    with patch('src.application.add_account.AddAccount.add') as mock_add_account, \
         patch('src.application.authentication.Authentication.auth') as mock_authentication:
        mock_add_account.return_value = None
        mock_authentication.side_effect = AccountNotFoundError()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 404

def test_sign_up_unexpected_error(client):
    with patch('src.application.add_account.AddAccount.add') as mock_add_account:
        mock_add_account.side_effect = TypeError()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 500

def test_sign_in_success(client):
    with patch('src.application.authentication.Authentication.auth') as mock_authentication:        
        mock_authentication.return_value = faker.words()
        response = client.post('/v1/sign-in', json={'email': email, 'password': password})
        assert response.status_code == 200
        assert 'accessToken' in response.json['data']

def test_sign_in_invalid_credentials_error(client):
    with patch('src.application.authentication.Authentication.auth') as mock_authentication:
        mock_authentication.side_effect = InvalidCredentialsError()
        response = client.post('/v1/sign-in', json={'email': email, 'password': password})
        assert response.status_code == 401

def test_sign_in_account_not_found_error(client):
    with patch('src.application.authentication.Authentication.auth') as mock_authentication:
        mock_authentication.side_effect = AccountNotFoundError()
        response = client.post('/v1/sign-in', json={'email': email, 'password': password})
        assert response.status_code == 404
