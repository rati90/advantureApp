from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from services.backend.app.db.session import get_db
from services.backend.app.internal.auth import authenticate_user, create_access_token, get_current_active_user
from services.backend.app.schemas import Token
from services.backend.app.schemas.user import User
from services.backend.app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

login = APIRouter(prefix="", tags=["Log"])


@login.post("/token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        user.username, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@login.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
