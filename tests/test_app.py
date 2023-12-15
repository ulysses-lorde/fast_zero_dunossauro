from fast_zero.schemas import UserPublic


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_error(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    data_update = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }

    response = client.put('/users/1', json=data_update)

    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_error(client):
    data_update = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }

    response = client.put('/users/2', json=data_update)

    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}
