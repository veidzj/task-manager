import pytest
from faker import Faker
from src.api.app import app
from unittest.mock import patch
from src.domain.errors.validation_error import ValidationError

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
         patch('src.application.authentication.Authentication.handle') as mock_authentication:
        mock_add_account.return_value = None
        mock_authentication.return_value = faker.words()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 201
        assert 'accessToken' in response.json['data']

def test_sign_up_validation_error(client):
    with patch('src.application.add_account.AddAccount.add') as mock_add_account, \
         patch('src.application.authentication.Authentication.handle') as mock_authentication:
        mock_add_account.side_effect = ValidationError(faker.words())
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 400

def test_sign_up_unexpected_error(client):
    with patch('src.application.add_account.AddAccount.add') as mock_add_account, \
         patch('src.application.authentication.Authentication.handle') as mock_authentication:
        mock_add_account.side_effect = TypeError()
        response = client.post('/v1/sign-up', json={'email': email, 'password': password})
        assert response.status_code == 500
