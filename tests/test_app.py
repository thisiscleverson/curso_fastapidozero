from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_returned_https_status_ok_and_hello_world(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World :)"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "Julia",
            "email": "julia@example.com",
            "password": "1234",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "Julia",
        "email": "julia@example.com",
    }


def test_try_create_user_with_username_alread_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "test",
            "email": "bob@example.com",
            "password": "1234",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_try_create_user_with_email_alread_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "bob",
            "email": "test@example.com",
            "password": "1234",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client, user):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        ]
    }


def test_read_users_returned_empty_list(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_read_user_by_user_id(client, user):
    response = client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def test_read_user_by_user_id_returned_not_found(client):
    response = client.get("/users/3")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "bob",
        "email": "bob@example.com",
    }


def test_update_user_returned_not_found_error(client):
    response = client.put(
        "/users/3",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f"/users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        "detail": "Username or Email already exists"
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User delete"}


def test_delete_user_not_found(client):
    response = client.delete("/users/3")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
