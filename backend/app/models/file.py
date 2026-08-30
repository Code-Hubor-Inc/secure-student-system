from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String

from app.db.database import Base
from app.models.base import BaseModel


class File(Base, BaseModel):
    __tablename__ = "files"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    storage_key = Column(String, nullable=False)
    encrypted_dek = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=True)
