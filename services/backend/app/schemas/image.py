from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class ImageBase(BaseModel):
    name: str
    file: bytes | None = None


class ImageCreate(ImageBase):
    ...


class Image(ImageBase):
    id: UUID
    item_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {bytes: lambda bs: "".join(map(chr, bs))}
