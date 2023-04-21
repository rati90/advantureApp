from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class AdventureBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)


class AdventureCreate(AdventureBase):
    ...

class AdventureUpdate(AdventureBase):
    ...

class Adventure(AdventureBase):
    id = UUID
    user_id = UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


