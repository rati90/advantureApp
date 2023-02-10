from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from services.backend.app.models.item import Image


class UserBase(BaseModel):
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str


class UserProfile(UserIn):
    name: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    surname: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    birthdate: datetime | None = None
    image: Image | None = None
