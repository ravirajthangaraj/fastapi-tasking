import datetime

import pytest

from main import application
from fastapi.testclient import TestClient
from app.utils.password import create_access_token

client = TestClient(application)


@pytest.fixture
def create_user_detail():
    return {
        'email': 'ravirajcse.2016@gmail.com',
        'first_name': 'Raviraj',
        'last_name': 'T',
        'username': 'ravirajt',
        'password': 'secret'
    }


@pytest.fixture
def jwt_test_headers(create_user_detail):
    token = create_access_token(create_user_detail, expires_delta=datetime.timedelta(minutes=2))
    return {'Authorization': f'Bearer {token}'}
