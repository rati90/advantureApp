from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from services.backend.app.models.item import Image


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: int
    disabled: bool | None = None


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    disabled: bool | None = None
    created_at: datetime
    updated_at: datetime
    name: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    surname: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    birthdate: datetime | None = None
    image: Image | None = None

    class Config:
        orm_mode = True
