from http import HTTPStatus


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

    print(response)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "Julia",
        "email": "julia@example.com",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "Julia",
                "email": "julia@example.com",
                "id": 1,
            }
        ]
    }


def test_read_user_by_user_id(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "Julia",
        "email": "julia@example.com",
    }


def test_read_user_by_user_id_returned_not_found(client):
    response = client.get("/users/3")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User delete"}


def test_delete_user_not_found(client):
    response = client.delete("/users/3")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
