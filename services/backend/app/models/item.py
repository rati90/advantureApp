from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    item_id: UUID
    name: str = Field(max_length=50)
    description: str = Field(max_length=250)
    price: float = None
    tax: float | None = None
    image: Image | None = None


class Adventure(BaseModel):
    adventure_id = str
    name: str = Field(max_length=50)
    description: str = Field(max_length=250)
    image: Image | None = None
    items: list[Item]


