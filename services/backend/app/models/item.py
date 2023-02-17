import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary, UUID
from sqlalchemy.orm import relationship
import uuid

from .mixins import Timestamp
from ..db.session import Base


class Item(Timestamp, Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=uuid), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(250))
    price = Column(Float, index=True)
    is_active = Column(Boolean, default=False)
    item_picture = Column(String, nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"), unique=True, nullable=True)

    owner = relationship("User", back_populates="item", uselist=False)
    image = relationship("Image", back_populates="item")


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=uuid), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, index=True, nullable=True)
    file = Column(LargeBinary)

    item_id = Column(UUID, ForeignKey("items.id"), unique=True, nullable=False)

    item = relationship("Item", back_populates="image")


