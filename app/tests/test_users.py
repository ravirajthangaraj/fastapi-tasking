
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_user_list():
    response = client.get('/users')
    assert response.status_code == 200
    assert type(response.json()) == list


def test_user_detail_by_email():
    response = client.get('/users/raviraj@gmail.com')
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_user_authenticate_without_data():
    response = client.post('/users/authenticate')
    assert response.status_code == 422
    assert type(response.json()) == dict


def test_user_authenticate_without_username():
    response = client.post('/users/authenticate', json={'password': 'secret'})
    assert response.status_code == 422
    assert type(response.json()) == dict


def test_user_authenticate_without_password():
    response = client.post('/users/authenticate', json={'username': 'ravirajt'})
    assert response.status_code == 422
    assert type(response.json()) == dict


def test_user_authenticate_wrong_username():
    response = client.post('/users/authenticate', json={'username': 'raviraj', 'password': 'secret'})
    assert response.status_code == 400
    assert type(response.json()) == dict


def test_user_authenticate_wrong_password():
    response = client.post('/users/authenticate', json={'username': 'ravirajt', 'password': 'sec'})
    assert response.status_code == 400
    assert type(response.json()) == dict