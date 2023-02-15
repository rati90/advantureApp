import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship


from .mixins import Timestamp
from ..db.session import Base


class Item(Timestamp, Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(250))
    price = Column(Float, index=True)
    is_active = Column(Boolean, default=False)
    image = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="item")



