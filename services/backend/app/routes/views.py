from typing import Any
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from services.backend.app.internal.auth import get_current_user, fake_users_db, authenticate_user, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from services.backend.app.models import UserBase, UserInDB, Adventure, Token


router = APIRouter(prefix="")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: UserBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]




@router.get("/home")
async def get_home():
    return {"home_page": "Welcome"}


@router.post("/user/", response_model=UserBase)
async def create_user(user: UserInDB) -> Any:
    return user


# @router.post("/user_profile/{profile_id}")
# async def get_profile(profile_id: str, profile: UserBase) -> User:
#     return profile


@router.post("/adventure/{adventure_id}")
async def get_adventure(adventure_id: str, adventure: Adventure) -> Adventure:
    return adventure
