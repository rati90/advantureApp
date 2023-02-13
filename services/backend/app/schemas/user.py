from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str
    role: int = 1
    is_active: bool = True


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True