from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr
from uuid import UUID


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: int = 1
    is_active: bool = True


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

