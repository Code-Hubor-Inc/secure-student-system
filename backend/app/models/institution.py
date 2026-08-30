from sqlalchemy import Boolean, Column, String

from app.db.database import Base
from app.models.base import BaseModel


class Institution(Base, BaseModel):
    __tablename__ = "institutions"

    name = Column(String, unique=True, nullable=False)
    domain = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
