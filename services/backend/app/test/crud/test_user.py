

from sqlalchemy.ext.asyncio import AsyncSession

from ...db import crud
from ...schemas import UserInDB
from ..utils.utils import random_email, random_lower_string


def test_create_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserInDB(email=email, hashed_password=password)
    user = crud.crud_user.create_user(db, user=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")