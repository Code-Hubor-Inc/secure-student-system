from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, LargeBinary

from app.db.database import Base
from app.models.base import BaseModel

class File(Base, BaseModel):
    __tablename__="files"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    institution_id = Column(ForeignKey("institutions.id"), nullable=True)

    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), unique=True, nullable=False)

    encrypted_dek = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)

    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=True)

    expires_at = Column(DateTime(timezone=True), nullable=True)