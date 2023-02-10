from typing import Any

from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends

from services.backend.app.models import UserBase, UserIn, Adventure
from services.backend.app.models.user import UserProfile

router = APIRouter(prefix="")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}



@router.get("/home")
async def get_home():
    return {"home_page": "Welcome"}


@router.post("/user/", response_model=UserBase)
async def create_user(user: UserIn) -> Any:
    return user


@router.post("/user_profile/{profile_id}")
async def get_profile(profile_id: str, profile: UserProfile) -> UserProfile:
    return profile


@router.post("/adventure/{adventure_id}")
async def get_adventure(adventure_id: str, adventure: Adventure) -> Adventure:
    return adventure
