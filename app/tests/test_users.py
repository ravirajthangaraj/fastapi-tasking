import os
from app.tests.conftest import client


def test_user_list_empty():
    response = client.get('/users/')
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) == 0


def test_user_detail_by_not_found_email():
    response = client.get('/users/ravirajcse.2016@gmail.com')
    assert response.status_code == 404
    assert type(response.json()) == dict


def test_user_create_with_no_data():
    response = client.post('/users/')
    assert response.status_code == 422


def test_user_create_only_with_name():
    response = client.post('/users/', json={
        'first_name': 'Raviraj'
    })
    assert response.status_code == 422


def test_user_create():
    response = client.post('/users/', json={
        'email': 'ravirajcse.2016@gmail.com',
        'first_name': 'Raviraj',
        'last_name': 'T',
        'username': 'ravirajt',
        'password': 'secret'
    })
    assert response.status_code == 200


def test_user_detail_by_email():
    response = client.get('/users/ravirajcse.2016@gmail.com')
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_user_list_with_one_data():
    response = client.get('/users/')
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) == 1


def test_authenticate_user_with_no_data():
    response = client.post('/users/authenticate/')
    assert response.status_code == 422


def test_authenticate_user_with_no_username():
    response = client.post('/users/authenticate/', json={
        "password": "secret"
    })
    assert response.status_code == 422


def test_authenticate_user_with_no_password():
    response = client.post('/users/authenticate/', json={
        "username": "ravirajt"
    })
    assert response.status_code == 422


def test_authenticate_user_with_invalid_username():
    response = client.post('/users/authenticate/', json={
        "username": "raviraj",
        "password": "secret"
    })
    assert response.status_code == 400
    assert response.json() == {"message": "Username/Password invalid"}


def test_authenticate_user_with_invalid_password():
    response = client.post('/users/authenticate/', json={
        "username": "ravirajt",
        "password": "secret1"
    })
    assert response.status_code == 400
    assert response.json() == {"message": "Username/Password invalid"}


def test_authenticate_user():
    response = client.post('/users/authenticate/', json={
        "username": "ravirajt",
        "password": "secret"
    })
    assert response.status_code == 200
    assert response.json()['username'] == 'ravirajt'
