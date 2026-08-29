from sqlalchemy import Column, String, Boolean, Integer, Text

from app.db.database import Base
from app.models.base import BaseModel


class Institution(Base, BaseModel):
    __tablename__ = "institutions"

    name = Column(String(255), nullable=False, unique=True)
    domain = Column(String(255), unique=True, nullable=True)
    address = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    max_users = Column(Integer, nullable=True)
    storage_limit = Column(Integer, nullable=True)
