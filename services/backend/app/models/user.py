import enum
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Boolean, Column, ForeignKey, String, Enum, Text
from sqlalchemy.orm import relationship
import uuid

from ..db.session import Base
from .mixins import Timestamp


class Role(enum.IntEnum):
    user = 1
    admin = 2


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=uuid), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(300), nullable=False)
    role = Column(Enum(Role))
    is_active = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="owner", uselist=False)
    item = relationship("Item", back_populates="owner")


class Profile(Timestamp, Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=uuid), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    bio = Column(Text, nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"), unique=True, nullable=True)

    owner = relationship("User", back_populates="profile")
