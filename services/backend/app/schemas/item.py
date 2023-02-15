from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class Image(BaseModel):
    name: str
    image: bytes | None = None


class ItemBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)
    price: float = None
    image: Image | None = None


class ItemCreate(ItemBase):
    ...


class Item(ItemBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Adventure(BaseModel):
    adventure_id = str
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)
    image: Image | None = None
    items: list[Item]


