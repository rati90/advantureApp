from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: str
    user_id: UUID


class ProfileCreate(ProfileBase):
    ...


class Profile(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True