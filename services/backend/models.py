from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class User(BaseModel):
    email: EmailStr


class UserProfile(User):
    name: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    surname: str = Field(min_length=1, max_length=50, regex="[a-zA-Z]+")
    birthdate: str
