import pytest
from faker import Faker
from unittest.mock import Mock
import jwt
from src.application.authentication import Authentication

faker = Faker()
email = faker.email()

@pytest.fixture
def setup_sut():
    user_repository_mock = Mock()
    secret_key = 'jwt_secret_key'
    sut = Authentication(user_repository_mock, secret_key)
    return sut, user_repository_mock, secret_key

def test_authentication_success(setup_sut):
    sut, user_repository_mock, secret_key = setup_sut

    user_repository_mock.get_by_email.return_value = {'email': email}

    token = sut.handle(email)

    decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])

    assert decoded_payload['email'] == email
    assert 'exp' in decoded_payload
