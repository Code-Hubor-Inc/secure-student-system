# Audit and Monitoring
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from app.core.database.base import BaseModel


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    action = Column(
        String(255), nullable=False
    )  # e.g 'login', 'file_upload', 'session_start'
    resource_type = Column(String(100), nullable=False)  # 'user', 'file', 'session'
    resource_id = Column(Integer, nullable=True)

    # Context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)

    # Details
    details = Column(JSON, nullable=True)  # Additonal context
    status = Column(String(50), nullable=False)
    severity = Column(
        String(50), default="info"
    )  # 'info', 'warning', 'error', 'critical'

    # Relationship
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, user_id{self.user_id})>"


class SecurityEvent(BaseModel):
    __tablename__ = "security_events"

    event_type = Column(
        String(255), nullable=False
    )  # 'failed_login', 'suspicious_download'
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    description = Column(Text, nullable=False)
    ip_address = Column(String(45), nullable=True)
    secerity = Column(String(50), nullable=False)  # 'low', 'medium', 'high', 'critical'
    resolved = Column(Boolean, default=False)
    resoution_notes = Column(Text, nullable=True)

    # Additional context
    metadata = Column(JSON, nullable=True)

    # Relationship
    user = relationship("User")

    def __repr__(self):
        return (
            f"<SecurityEvent(id={self.id}, event_type={self.event_type}, "
            f"severity={self.severity})>"
        )
