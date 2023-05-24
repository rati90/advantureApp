from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(max_length=50)


class CategoryCreate(CategoryBase):
    ...


class CategoryUpdate(CategoryBase):
    ...


class Category(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
