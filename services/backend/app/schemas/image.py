from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, errors
from typing import Any, Callable, Generator


def hex_bytes_validator(val: Any) -> bytes:
    if isinstance(val, bytes):
        return val
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, str):
        return bytes.fromhex(val)
    raise errors.BytesError()


class HexBytes(bytes):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield hex_bytes_validator


class ImageBase(BaseModel):
    name: str
    file: bytes | None = None


class ImageCreate(ImageBase):
    ...


class ImageUpdate(ImageBase):
    ...


class Image(ImageBase):
    id: UUID
    item_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {bytes: lambda bs: bs.hex()}
