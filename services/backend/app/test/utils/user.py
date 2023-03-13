from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from .utils import random_email, random_lower_string

from ... import settings
from ...models import User
from ...schemas import UserInDB, UserUpdate
from ...db import crud


def user_authentication_headers(
    *, client: TestClient, email: EmailStr, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserInDB(username=email, email=email, hashed_password=password)
    user = crud.crud_user.create_user(db=db, user=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: EmailStr, db: AsyncSession
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.crud_user.get_user_by_email(db, email=email)
    if not user:
        user_in_create = UserInDB(username=email, email=email, hashed_password=password)
        user = user =  crud.crud_user.create_user(db=db, user=user_in_create)
    # else:
    #     user_in_update = UserUpdate(password=password)
    #     user = crud.crud_user.update(db, db_obj=user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)