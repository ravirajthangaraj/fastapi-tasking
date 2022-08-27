import os
from app.tests.conftest import client, create_user_detail, jwt_test_headers


def test_endpoint_without_bearer_token():
    # authenticated endpoint
    response = client.get('/users/')
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


def test_endpoint_without_invalid_token_scheme():
    # authenticated endpoint
    response = client.get('/users/', headers={'Authorization': 'testauth'})
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


def test_endpoint_without_invalid_token():
    # authenticated endpoint
    response = client.get('/users/', headers={'Authorization': 'Bearer testauth'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authorization required'}


def test_user_create_with_no_data():
    response = client.post('/users/signup/')
    assert response.status_code == 422


def test_user_create_only_with_name():
    response = client.post('/users/signup/', json={
        'first_name': 'Raviraj'
    })
    assert response.status_code == 422


def test_user_create(create_user_detail):
    response = client.post('/users/signup/', json=create_user_detail)
    assert response.status_code == 200


def test_user_detail_by_not_found_email(jwt_test_headers):
    response = client.get('/users/ravirajcse2016@gmail.com', headers=jwt_test_headers)
    assert response.status_code == 404
    assert type(response.json()) == dict


def test_user_detail_by_email(jwt_test_headers):
    response = client.get('/users/ravirajcse.2016@gmail.com', headers=jwt_test_headers)
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_user_list_with_one_data(jwt_test_headers):
    response = client.get('/users/', headers=jwt_test_headers)
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


def test_authenticate_user(create_user_detail):
    response = client.post('/users/authenticate/', json={
        "username": create_user_detail.get('username'),
        "password": create_user_detail.get('password')
    })
    assert response.status_code == 200
    assert response.json()['access_token'] != ''


"""Execute after deleting the created user"""
# def test_user_list_empty(jwt_test_headers):
#     response = client.get('/users/', headers=jwt_test_headers)
#     assert response.status_code == 200
#     assert type(response.json()) == list
#     assert len(response.json()) == 0
