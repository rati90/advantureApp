from pydantic import BaseModel, Field, HttpUrl
from pydantic.networks import EmailStr


class User(BaseModel):
    email: EmailStr


class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=250)
    price: float = None
    tax: float | None = None
    image: Image | None = None


class UserProfile(User):
    name: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    surname: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    birthdate: str
    image: Image | None = None


class Adventure(BaseModel):
    adventure_id = str
    name: str = Field(max_length=50)
    description: str = Field(max_length=250)
    image: Image | None = None
    items: list[Item]
