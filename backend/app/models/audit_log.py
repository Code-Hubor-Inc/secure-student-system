from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
import enum

from app.db.database import Base
from app.models.base import BaseModel

class AuditAction(str, enum.Enum):
    register = "register"
    login = "login"
    upload = "upload"
    download = "download"
    delete = "delete"

class AuditLog(Base, BaseModel):
    __tablename__="audit_logs"

    user_id = Column(ForeignKey("users.id"), nullable=True)
    action = Column(Enum(AuditAction), nullable=False)
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)