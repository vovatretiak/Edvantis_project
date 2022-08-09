import pytest

from project.users.models import User
from project.utils import get_password_hash


@pytest.fixture(autouse=True)
def create_dummy_users():
    """fixture to execute asserts before and after a test is run"""

    from .db_for_tests import override_get_db

    db = next(override_get_db())
    new_user = User(
        username="john123",
        email="john123@mail.com",
        password=get_password_hash("password"),
    )
    db.add(new_user)
    db.commit()
    new_user2 = User(
        username="jane123",
        email="jane123@mail.com",
        password=get_password_hash("password2"),
    )
    db.add(new_user2)
    db.commit()
    yield

    # teardown
    db.query(User).filter(User.username == "john123").delete()
    db.query(User).filter(User.username == "jane123").delete()
    db.commit()
