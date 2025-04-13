from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="maria", password="senha123", email="maria@example.com"
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == "maria"))

    assert asdict(user) == {
        "id": 1,
        "username": "maria",
        "password": "senha123",
        "email": "maria@example.com",
        "created_at": time,
        "updated_at": time,
    }
