from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID


class Image(BaseModel):
    url: HttpUrl
    name: str


class ItemBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)
    price: float = None
    #    image: Image | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID
    owner_id: UUID


    class Config:
        orm_mode = True



class Adventure(BaseModel):
    adventure_id = str
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)
    image: Image | None = None
    items: list[Item]


