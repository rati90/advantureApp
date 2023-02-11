from pydantic import BaseModel
from datetime import datetime


class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: str
    user_id: int


class ProfileCreate(ProfileBase):
    ...


class Profile(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True